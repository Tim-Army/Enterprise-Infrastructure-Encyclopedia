# Chapter 09: NAC, Dynamic Port Policies, Quarantine, and Multicast

## Learning Objectives

- Explain how a FortiGate learns about the devices behind a managed
  FortiSwitch (**device detection**: MAC cache, LLDP, DHCP snooping, network
  monitoring, and the FortiGuard IoT service) and read the result with
  `diagnose user device list`.
- Build a **FortiSwitch NAC policy** with a **MAC policy**, put a port in NAC
  mode, watch an unknown device land in the **onboarding VLAN** and a matched
  device move to its assigned VLAN, and use the NAC policy's **dynamic firewall
  address** in a firewall policy; explain what **NAC LAN segments** add and why
  the FS-108F cannot use them when cabled directly to the FortiGate (feature
  matrix note 12).
- Build a **dynamic port policy** whose rule matches a device by MAC address or
  hardware vendor and applies a **VLAN policy**, an **LLDP profile**, and a
  **QoS policy** to the port, and state how it differs from NAC.
- **Quarantine** a host by MAC address in quarantine-by-VLAN mode, see it move
  to the quarantine VLAN and its DHCP server, release it, use
  `bounce-quarantined-link` and `drop`, and read a quarantined 802.1X MAC-based
  session; predict quarantine-by-redirect.
- Enable **IGMP snooping**, the **IGMP-snooping proxy**, and the **querier** on a
  FortiSwitch VLAN from the FortiGate, see unregistered multicast pruned and a
  joined group forwarded, control flooding per switch and per port, check MCLAG
  IGMP-snooping awareness on S3, and state the FS-1xx limits (note 23) and why
  **MLD snooping** is read-and-predict on every switch option.

## Theory and Architecture

### Where each feature lives in FortiLink mode

Everything in this chapter is configured on the FortiGate. The table maps each
feature to its FortiOS objects (FortiOS 7.6.0 CLI Reference; FortiLink Guide
7.6.7, pp. 146–149, 164–172, 182–216, and 263–272):

| Feature | FortiOS object | Key options |
| --- | --- | --- |
| Device detection | `config system interface` (the FortiSwitch VLAN); `config switch-controller global`; `config switch-controller network-monitor-settings` | `device-identification`; `update-user-device`; `network-monitoring` |
| FortiGuard IoT detection | `config switch-controller system`; `config system interface` (the FortiLink interface) | `iot-weight-threshold`, `iot-scan-interval`, `iot-holdoff`, `iot-mac-idle`; `switch-controller-iot-scanning` |
| NAC settings | `config switch-controller fortilink-settings`, `config nac-ports` | `onboarding-vlan`, `lan-segment`, `nac-lan-interface`, `nac-segment-vlans`; `inactive-timer`, `link-down-flush` |
| NAC policy | `config user nac-policy` | `category`, match fields (`mac`, `hw-vendor`, `family`, `type`, `os`, `host`, `user`, `user-group`, `ems-tag`, `severity`), `switch-fortilink`, `switch-group`, `switch-mac-policy`, `firewall-address`, `match-type`, `match-period` |
| MAC policy (the NAC action) | `config switch-controller mac-policy` | `fortilink`, `vlan`, `traffic-policy`, `count`, `bounce-port-link` |
| NAC port | `config switch-controller managed-switch`, `config ports` | `access-mode nac` |
| Dynamic port policy | `config switch-controller dynamic-port-policy`, `config policy`; `config switch-controller vlan-policy` | Match: `category`, `mac`, `host`, `hw-vendor`, `type`, `family`, `interface-tags`; actions: `vlan-policy`, `lldp-profile`, `qos-policy`, `802-1x`, `bounce-port-link` |
| Dynamic port | `config ports`; `config system interface` (the FortiLink interface) | `access-mode dynamic`, `port-policy`; `switch-controller-dynamic` |
| Engine intervals | `config switch-controller system` | `nac-periodic-interval`, `dynamic-periodic-interval` (both 5–180 s, default 60) |
| Quarantine | `config user quarantine`; `config switch-controller global` | `quarantine`, `config targets`, `config macs`, `drop`, `traffic-policy`, `firewall-groups`; `quarantine-mode`, `bounce-quarantined-link` |
| IGMP snooping | `config system interface` (per VLAN); `config switch-controller igmp-snooping` (global); managed-switch `config igmp-snooping` (per switch, per VLAN); `config ports` (per port) | `switch-controller-igmp-snooping`, `-proxy`, `-fast-leave`; `aging-time`, `flood-unknown-multicast`, `query-interval`; `local-override`, `querier`, `querier-addr`, `version`; `igmp-snooping-flood-reports`, `mcast-snooping-flood-traffic`; `mclag-igmp-snooping-aware` |

### Device detection

NAC and dynamic port policies match devices, so the FortiGate must first know
them. Three sources feed its device list:

- **The FortiGate's own device identification** on the VLAN interface
  (`device-identification enable`, set on `fsw-users` to `fsw-guest` in
  Chapter 04), which fingerprints traffic that reaches the FortiGate.
- **Information from the managed switch.** `update-user-device` under `config
  switch-controller global` chooses which switch databases update the device
  list; the FortiOS 7.6.0 default is all five: `mac-cache`, `lldp`,
  `dhcp-snooping`, `l2-db`, and `l3-db`. The `lldp` source is how a device's
  LLDP advertisements reach the FortiGate: FortiSwitchOS parses LLDP messages
  from voice devices such as FortiFone and passes them on for device detection
  (FortiLink Guide 7.6.7, p. 164).
- **Network-assisted device detection** (`network-monitoring enable` under
  `config switch-controller network-monitor-settings`, default `disable`),
  which lets the switch passively gather information about other devices
  (p. 164). The feature matrix's "Network device detection" row is a dash in the
  1xxE/1xxF column and a chain in the 200 Series column, so it is hands-on only
  on S3.

The list is read with `diagnose user device list` (p. 164), or in the GUI under
the Device Inventory. The values that NAC and dynamic port policies can match
(hardware vendor, type, family, operating system) are published in a Fortinet
JSON list that the guide links (pp. 188, 211).

**FortiGuard IoT detection** identifies Internet of things devices from their
MAC addresses through a FortiGuard service and needs an **IoT Detection Service
license** (pp. 171–172). It is disabled by default on the FortiLink interface
(`switch-controller-iot-scanning`); the scan timers are under `config
switch-controller system` (`iot-scan-interval` default 60 minutes,
`iot-holdoff` 5, `iot-mac-idle` 1,440, `iot-weight-threshold` 1; 0 disables
each). The C2 evaluation has no such license, and this volume assumes none, so
the chapter only reads the settings. The matrix marks FortiGuard IoT
identification as supported in both modes in both columns.

### FortiSwitch NAC

**FortiSwitch network access control (NAC)** matches devices on NAC-mode ports
against NAC policies and applies the matched policy's action, normally a
different VLAN, to that device (FortiLink Guide 7.6.7, pp. 182–210). The
sequence on a NAC port is:

1. A new MAC address appears on a port with `access-mode nac`. Until it
   matches a policy it is placed in the **onboarding VLAN** (the auto-created
   `onboarding` interface, VLAN 4089, which has no address in this lab's
   templates; Chapter 03).
2. The NAC engine runs every `nac-periodic-interval` seconds (default 60) and on
   events. When the device matches an enabled NAC policy, it is authorized
   automatically and the policy's **MAC policy** assigns it a VLAN (and
   optionally a traffic policy and packet counting).
3. If the policy names a **dynamic firewall address** (`type dynamic`,
   `sub-type swc-tag`), the device's MAC address joins that address, so
   firewall policies can refer to "whatever matched this NAC policy" (from
   FortiOS 7.0.1; pp. 189–191).

Key settings and defaults:

| Setting | Where | Default and meaning |
| --- | --- | --- |
| NAC settings entry | `config switch-controller fortilink-settings`, `edit <FortiLink interface>` | Created automatically when the first switch is discovered; otherwise create it before any NAC policy (p. 183) |
| `onboarding-vlan` | `config nac-ports` | None assigned by default (p. 184); this lab sets `onboarding` |
| `inactive-timer` | Entry | 15 minutes (1–1,440) that NAC devices may stay inactive |
| `link-down-flush` | Entry | `enable` in the 7.6.0 reference: a link-down clears NAC and dynamic devices from the port |
| `nac-periodic-interval` | `config switch-controller system` | 60 s (5–180) |
| Port bounce | MAC policy `bounce-port-link` (7.6.0, default `enable`) | Bouncing the port restarts the device's DHCP, which changes its address and invalidates firewall sessions (p. 184) |
| `match-type`, `match-period` | NAC policy | `dynamic`: matches are removed on link-down, inactivity, or switch offline; `override` keeps them for `match-period` days (0 = forever, up to 120), from FortiOS 7.4.4 (p. 189) |

NAC policies are matched **in the order listed** and reordered with `move`
(p. 188). The 7.6.0 reference gives five categories: `device` (the default:
MAC address, hardware vendor, family, type, operating system, host, user),
`firewall-user` (a user group), `ems-tag` (a FortiClient EMS tag),
`fortivoice-tag`, and `vulnerability` (IoT and OT severity, which needs an Attack
Surface Security Rating license). The guide adds that a NAC policy may name
FortiSwitch groups (`switch-group`; none means all), and that from FortiOS
7.2.4 with FortiSwitchOS 7.2.2 NAC supports up to 48 times the controller's
maximum number of managed switches as known devices (p. 188).

Three diagnostics show the result (FortiLink Guide 7.6.7, pp. 203–204):

| Command | Shows |
| --- | --- |
| `diagnose switch-controller mac-device nac known` | Devices that matched a NAC policy: MAC, last switch and port, matched policy, MAC policy, last seen |
| `diagnose switch-controller mac-device nac onboarding` | Devices with no matching policy, and where they are |
| `diagnose switch-controller mac-device cache` | The controller's event cache: switch, MAC, VLAN, ages, interface |
| `execute switch-controller get-nac-mac-cache` (on the switch) | The switch's NAC cache: MAC, VLAN, ACT, SYNC, interface (FortiSwitchOS 7.6.7 CLI Reference, p. 451) |

**NAC device telemetry** (FortiOS 7.2.4 with FortiSwitchOS 7.2.3) counts packets
and bytes per known device when the MAC policy has `count enable`, read with
`diagnose switch-controller telemetry show mac-stats` (pp. 204–205). The matrix
row is a dash in the 1xxE/1xxF column and a chain in the 200 Series column, and
the guide's model list names the FS-224E, FS-224E-POE, FS-224D-FPOE, FS-248D,
FS-248E-POE, and FS-248E-FPOE but not the plain FS-248E; record what an S3 pair
of FS-248E switches prints.

**NAC with 802.1X on the same port** (the NAC user policy checked after an
802.1X MAC-based authentication) is a FortiOS 7.6.4 feature (pp. 233–234); FGT-1
runs 7.6.2, so this volume only reads about it. Port-based 802.1X is not
supported with it.

### Where the FortiLink Guide and the FortiOS 7.6.0 reference differ

| Guide (FortiOS 7.6.7) | FortiOS 7.6.0 CLI Reference | This chapter |
| --- | --- | --- |
| `set bounce-nac-port` under `config nac-ports` (pp. 186, 213) | No such option; `bounce-port-link` is in the MAC policy and in each dynamic port policy rule | Uses the 7.6.0 options |
| `set switch-auto-auth` in every NAC policy syntax block (pp. 192–202) | Not in `config user nac-policy` | Not used |
| `set nac-lan-interfaces` in the syntax line, `nac-lan-interface` in the example (pp. 186–187) | `nac-lan-interface` | Singular |
| User policy `set category firewall-user user` (p. 193) | `category` takes one value: `firewall-user` | `firewall-user` |
| IGMP snooping cannot be used with NAC enabled globally by `set mode global` under `config switch-controller nac-settings` (p. 146) | No `config switch-controller nac-settings` table | Record it if your build has one; Lab 9.4 runs with NAC off |
| Quarantine example sets `description` directly under `config macs` (p. 266) | `description` exists at the target level and per MAC entry | Sets it at the target level |

### NAC LAN segments

When NAC moves a device to a new VLAN by bouncing the port, the device's address
changes and its sessions break. **LAN segments** (FortiOS 7.0.1 with
FortiSwitchOS 7.0.1) avoid that: the segment VLANs share the primary NAC
segment interface's address and DHCP server (the auto-created `nac_segment`
interface, `10.255.13.1/24` in Chapter 01), so a device keeps its address while
the switch still isolates the segments (FortiLink Guide 7.6.7, pp. 184–187,
206–210). The rules are strict:

- The FortiGate supports **only one** LAN segment.
- Segment VLANs carry no Layer 3 properties: no address, `allowaccess`, or DHCP
  server, and access mode `static`. An RSPAN VLAN cannot be a member.
- Do not change VLANs after assigning them to a segment (p. 186).
- With IGMP snooping in a segment, enable it on every VLAN in the segment,
  primary, sub-VLANs, and onboarding; multicast streams must enter only on the
  primary VLAN (FortiOS 7.2.0 with FortiSwitchOS 7.2.0, p. 186).
- **Note 12 models**, including the **FS-108F** and its POE and FPOE variants,
  the FS-124E family, and the FS-148E: FortiSwitchOS assigns an internal VLAN
  (`lan-internal-vlan`) that nothing else may use; these models **cannot be
  directly connected to a FortiGate** and should be connected through another
  FortiSwitch model; FortiSwitchOS 7.2.0 or later is required; all segment VLANs
  must be in the same STP instance; and MAC learning happens on the internal
  VLAN (pp. 185–186).

So LAN segments are **read-and-predict on every option** in this volume: the lab
VLANs have addresses and DHCP and would have to be rebuilt, C2 cannot add the
interfaces, and S1 is cabled straight to the controller, which note 12
excludes. The FS-124F (S2) and the 200 Series (S3) are not in note 12.

### Dynamic port policies

A **dynamic port policy (DPP)** changes a **port's** properties according to
the device that appears on it (FortiLink Guide 7.6.7, pp. 164–171, 211–216).
Its rules are processed from first to last; the last rule should hold the
default properties for any port with this policy, and from FortiOS 7.4.4
devices match by rule priority instead of first come, first served (p. 214).
Each rule matches a `category device` pattern (`mac`, `host` name or IP address,
`hw-vendor`, `type`, `family`) or `category interface-tag` (`interface-tags`)
and applies any of:

| Action | Object it names | Effect on the port |
| --- | --- | --- |
| `vlan-policy` | `config switch-controller vlan-policy`: `vlan` (native), `allowed-vlans`, `untagged-vlans`, `allowed-vlans-all`, `discard-mode` | The port's VLANs |
| `lldp-profile` | An LLDP profile (Chapter 10 builds its own) | What the port advertises, including LLDP-MED voice VLANs |
| `qos-policy` | `config switch-controller qos qos-policy` | Trust maps and queue policy |
| `802-1x` | An 802.1X security policy (Chapter 07) | Authentication on the port |
| `bounce-port-link` | — | Default `enable` in 7.6.0: bounce the link so the device renews its VLAN and address |

Three pieces turn it on: the FortiLink interface names the NAC settings entry
in `switch-controller-dynamic` (p. 212), the port takes `access-mode dynamic`
and `port-policy <DPP>`, and the DPP and its objects name the same `fortilink`.
The engine runs every `dynamic-periodic-interval` seconds (default 60). The
guide's voice example matches `family "FortiFone"` and applies the predefined
`fortivoice.fortilink` LLDP profile and `voice-qos` QoS policy with a VLAN
policy (pp. 169–170); `diagnose switch-controller mac-device dynamic` then shows
the device with its dynamic port policy and rule (p. 171), and the port shows
the matched rule in its read-only `matched-dpp-policy`.

**NAC or DPP?**

| | NAC policy | Dynamic port policy |
| --- | --- | --- |
| Acts on | The **device** (its MAC address goes into a VLAN) | The **port** (its native and allowed VLANs, LLDP, QoS, 802.1X) |
| Port mode | `access-mode nac` | `access-mode dynamic` with `port-policy` |
| Unmatched device | Onboarding VLAN | Not documented (Lab 9.2's negative test records it); the guide says the last rule should hold the default properties |
| Firewall integration | Dynamic firewall address (`swc-tag`) | None directly |
| Typical use | Sort unknown devices into VLANs by identity | Configure a port for whatever is plugged in, such as a phone |

### Quarantine

A **quarantine** isolates hosts by MAC address (FortiLink Guide 7.6.7,
pp. 263–272). FortiOS 7.6 configures it in `config user quarantine`; the guide
notes that the feature used to be `config switch-controller quarantine`, and the
7.6.0 reference still documents both tables (the old one with `tag` per MAC and
a default of `disable`, the new one with `drop` per MAC and a default of
`enable`). This chapter uses `config user quarantine`. Two modes are set by
`quarantine-mode` under `config switch-controller global`:

| Mode | Behavior | Since |
| --- | --- | --- |
| `by-vlan` (default from FortiOS 6.4.1) | The quarantined MAC address is moved to the **quarantine VLAN** (4093) on the switch and its traffic goes to the FortiGate there | FortiOS 6.0.0 |
| `by-redirect` | The traffic stays in its VLAN but is redirected to the FortiGate, matched by the firewall address group `QuarantinedDevices` | FortiOS 6.4.0 |

Changing to `by-redirect` means disabling quarantine, changing the mode,
**removing the quarantine VLAN from the switch ports**, and enabling quarantine
again (p. 264). This volume keeps `quarantine` in every port's allowed list
(Chapter 04), so by-redirect is read-and-predict here.

| Option | Default and meaning |
| --- | --- |
| `quarantine` | `enable`; MAC addresses added while it is disabled are quarantined only once it is enabled again (p. 264) |
| `config targets`, `edit <entry>` | Up to 512 entries; any number of MAC addresses per entry |
| `config macs`, `edit <MAC>`, `drop` | `disable` sends the device's traffic to the FortiGate; `enable` blocks it |
| `firewall-groups` | Address group holding all quarantined MAC addresses; default `QuarantinedDevices`, required with by-redirect |
| `traffic-policy` | Optional `config switch-controller traffic-policy` (policer, guaranteed bandwidth and burst, CoS queue) for quarantined devices |
| `bounce-quarantined-link` (`config switch-controller global`) | `disable`; when enabled, the port where the device was last seen goes down and up at quarantine and at release, so a DHCP client renews into the right network (p. 267) |

The **quarantine VLAN interface** is an **access VLAN**
(`switch-controller-access-vlan enable`) with `security-mode captive-portal`, and
the guide's example gives it its own DHCP server (pp. 270–271). In this lab it is
the auto-created `quarantine` interface, `10.255.11.1/24` (Chapter 03). The
guide's quarantine pages show an older naming, `qtn.<FortiLink port>` with
`10.254.254.254/24`, and say that with several FortiLink interfaces only the
first quarantine VLAN gets that address (p. 263); record which naming and
address your controller shows.

On the switch, the controller pushes a **MAC-to-VLAN binding**: `show switch
vlan 4093` lists the MAC address under `config member-by-mac`, and `diagnose
switch vlan assignment mac list` shows it in VLAN 4093 (pp. 268–269). For a
device authorized by **802.1X MAC-based** authentication, the session output
shows the quarantined MAC address with VLAN 4093 in a `Quarantined` column,
because quarantine-VLAN detection (`quarantine-vlan`) is enabled by default on
the switch, globally and per port (pp. 267–268). Released devices leave
quarantine when their MAC address, their entry, or the whole feature is removed
(p. 272).

The guide's switch-side example shows VLAN 4093 with both `dhcp-snooping enable`
and `access-vlan enable` (p. 268). The FortiSwitchOS 7.6.7 Administration Guide
says that only from **FortiSwitchOS 7.6.5** can DHCP snooping, ARP inspection,
and access VLAN be enabled together on one switch VLAN (p. 276). On an earlier
build, do not add DHCP snooping or DAI to the quarantine VLAN yourself; Lab 9.3
records what the switch shows.

### IGMP snooping, the querier, and multicast flood control

**IGMP snooping** lets the switch listen to IGMP between hosts and routers and
forward each multicast group only to ports with a listener (FortiLink Guide
7.6.7, pp. 146–149; FortiSwitchOS 7.6.7 Administration Guide, pp. 312–318).
The switch keeps one entry per VLAN per group, adds a port when a host joins,
and removes it when the last host leaves or the entry ages out. Without a
**querier**, hosts send reports only when they join (and in answer to queries),
so entries age out; the managed switch can act as querier when no external
querier is present, sending version 2 (default) or version 3 queries.
**Unregistered** multicast (a group nobody has joined) is forwarded only to
multicast router (mRouter) ports or to interfaces with
`mcast-snooping-flood-traffic enable`, unless `flood-unknown-multicast` is
enabled (Administration Guide, p. 313).

In FortiLink mode the settings sit at four levels:

| Level | Object | Options and defaults (FortiOS 7.6.0) |
| --- | --- | --- |
| VLAN | `config system interface` | `switch-controller-igmp-snooping`, `-igmp-snooping-proxy`, `-igmp-snooping-fast-leave`, all `disable` |
| Global | `config switch-controller igmp-snooping` | `aging-time` 300 (15–3,600 s), `flood-unknown-multicast disable`, `query-interval` 125 (10–1,200 s, FortiOS 7.2.1 and later) |
| Per switch and VLAN | managed-switch `config igmp-snooping`, `config vlans` | `local-override disable` (must be `enable` to override `aging-time` and `flood-unknown-multicast`, and for the querier); per VLAN `proxy global`, `querier disable`, `querier-addr`, `version` (2) |
| Per port | `config ports` | `igmp-snooping-flood-reports disable`, `mcast-snooping-flood-traffic disable` |

The guide requires IGMP snooping on the VLAN before the proxy, and snooping and
the proxy before the querier (p. 148). `aging-time` must be greater than
`query-interval`. The switch-side reference gives a `query-interval` default of
120 under `config switch igmp-snooping globals` (FortiSwitchOS 7.6.7 CLI
Reference, p. 125), the FortiOS reference 125; Lab 9.4 records what the switch
receives.

Limits and quirks that shape the lab:

- **Note 23:** on the FS-1xxE/F/G series (S1, S2), IGMP snooping can be enabled
  on at most **5 VLANs** (also Administration Guide, p. 313).
- **239.x.x.x floods** within the VLAN on the FS-124F (all variants), FS-148F,
  FS-110G-FPOE, and FS-124G models (FortiLink Guide 7.6.7, p. 147). The lab
  therefore uses a group from the documentation block `233.252.0.0/24` (RFC
  5771), `233.252.0.174`, and tests 239 separately on S2.
- When an ISL forms automatically, the two flood options are disabled on it.
- **Proxy reporting is not supported for IGMPv3**, explicit host tracking and
  IGMPv3 immediate leave are not supported, and the proxy's reports and leaves
  use the address `0.0.0.0` (Administration Guide, p. 314). Linux hosts send
  IGMPv3 reports by default, and fall back to version 2 when they hear version 2
  queries.
- Snooping table limits: 1,000 groups on the FS-124F, FS-224E, FS-248D, and
  FS-248E (p. 314); the FS-108F is not in the table, so read `Max multicast
  snooping groups` from `get switch igmp-snooping status`.
- **MCLAG (S3):** `mclag-igmpsnooping-aware` must be enabled on the switches,
  and the flood options must be disabled on ISL and FortiLink trunks and enabled
  on ICL trunks (FortiLink Guide 7.6.7, p. 85). The sources disagree on its
  default: the guide says enabled, the FortiSwitchOS 7.6.7 CLI Reference says
  `disable` (p. 118), and the FortiOS 7.6.0 managed-switch option that pushes it,
  `mclag-igmp-snooping-aware` (note the extra hyphen), defaults to `enable`.
  Lab 9.4 reads it on both switches before enabling snooping.

**MLD snooping** is the IPv6 equivalent. In the 7.6.7 feature matrix, MLD
snooping, proxy, and querier are a dash in both the 1xxE/1xxF and 200 Series
columns (standalone-only on the 500, 10xx, 2048F, and 3032 models), and the
FortiOS 7.6.0 reference has no MLD option for managed switches; the switch-side
VLAN options (`mld-snooping`, `-querier`, `-proxy`) exist only in standalone
FortiSwitchOS. MLD is therefore read-and-predict on every option. Where both
IGMP and MLD hosts exist, the Administration Guide asks for both snooping types
or neither on a VLAN, because unregistered IPv4 and IPv6 multicast share one
flooding behavior in hardware (p. 313).

### Model support for this chapter

From the FortiSwitchOS 7.6.7 feature matrix (`temp/nse5fsw/fm767.txt`, the
position-based read); chain = standalone and managed, check = standalone only,
dash = not supported:

| Feature | 1xxE/1xxF (S1 FS-108F, S2 FS-124F) | 200 Series (S3) | Note |
| --- | --- | --- | --- |
| Device detection | Chain | Chain | |
| Network device detection | Dash | Chain | |
| Integrated FortiGate NAC | Chain | Chain | |
| NAC LAN segments | Chain | Chain | Note 12: FS-108F family, FS-124E family, FS-148E (and FSR models) have limits, including no direct connection to a FortiGate |
| FortiGuard IoT identification | Chain | Chain | Needs an IoT Detection Service license |
| EMS tags, IoT/OT vulnerabilities, FortiVoice tags in NAC policies | Chain | Chain | Need EMS, a Security Rating license, or FortiVoice |
| NAC and DPP: control of how long matched devices are kept | Chain | Chain | FortiOS 7.4.4 |
| NAC and 802.1X on the same port | Chain | Chain | FortiOS 7.6.4: read-only on FGT-1 |
| Dynamic port policies | Chain | Chain | |
| NAC device telemetry | Dash | Chain | Guide's model list omits the plain FS-248E |
| Host quarantine | Chain | Chain | |
| IGMP snooping, IGMP proxy, IGMP querier | Chain | Chain | Note 23: 5 VLANs on FS-1xxE/F/G |
| IGMP snooping support in MCLAG | Dash | Chain | |
| MLD snooping, proxy, querier | Dash | Dash | |

## Design Considerations

### Exam tasks this chapter practices

| Exam task | Labs here | Track 2 mode |
| --- | --- | --- |
| 3.3 ACLs, security profiles, VLAN security | 9.1, 9.3 (primary) | Build + predict |
| 1.2 QoS and LLDP-MED | 9.2 (LLDP profile and QoS policy as DPP actions) | Build + predict |
| 2.1 Configure and provision | 9.2 (ports provisioned by device) | Build + predict |
| 4.3 View and extract information | 9.1–9.4 (device list, NAC and DPP device tables, IGMP groups) | Predict |
| Course-only topics | 9.3 (quarantine), 9.4 (IGMP snooping) | Build + predict |

### Hosts, ports, and VLANs

| Lab | Port and host | VLAN plan |
| --- | --- | --- |
| 9.1 NAC | `port2`, endpoint B (static `10.174.43.20/24`) | Onboarding VLAN 4089 until matched, then `fsw-iot` by the MAC policy |
| 9.2 DPP | `port2`, endpoint B | `fsw-iot` native through a VLAN policy that also allows `quarantine` |
| 9.3 Quarantine | `port1`, endpoint A (DHCP in `fsw-users`); optionally `port2` with 802.1X | `fsw-users`, then quarantine VLAN 4093 |
| 9.4 IGMP | `port1` endpoint A (receiver), `port2` endpoint B (sender) | Both in `fsw-users`; `port2` moves there temporarily with `10.174.41.20/24`, as in Chapter 08 |

NAC matches endpoint B by MAC address. A match by vendor or operating system
needs the FortiGate to have identified the device first, and a device sitting
in an onboarding VLAN with no address sends almost nothing the FortiGate can
fingerprint; the MAC address is the one attribute the switch always reports.
Lab 9.2 then tries a vendor match from the device list as well.

`port1` and `port2` keep BPDU guard (Chapter 05); nothing here plugs a bridge
into them. Port changes use `set vlan`, `access-mode`, and `port-policy`, never
`set allowed-vlans`; if a mode change alters the allowed or untagged lists,
the rollback puts `quarantine` back with `append`. Chapter 08 left `port1` with
`discard-mode none`, which Lab 9.3 needs.

### The FortiLink interface name

Commands below are written for C2, where the FortiLink interface is `port3`. On
C3 use `port4`, and on C1 `<FL_PORT>` (or `fortilink`), as in Chapter 04. The
NAC settings entry under `config switch-controller fortilink-settings` is named
after the FortiLink interface (p. 186); Lab 9.1 records its name as
`<FL_SETTINGS>`.

### The C2 budget and the lab-VLAN NO-GO

No lab adds an interface or a route. Lab 9.1 Part C uses **P3**, the C2
evaluation's one free policy slot, for a policy from `FSW-LAN` to `FSW-LAN`
whose source is the NAC policy's dynamic address and whose destination is an
address object for `fsw-users`; its rollback deletes both. Address objects, NAC
and MAC policies, VLAN and dynamic port policies, quarantine entries, and IGMP
settings do not count against the caps. If Lab 4.1 sent you down the branch
that uses P3 for an internet policy, Lab 9.1 Part C is read-and-predict on C2.
After a C2 lab-VLAN NO-GO, Chapter 04 sends this chapter to C1 or C3.

### Lab order and state

| Lab | Builds | Rollback leaves |
| --- | --- | --- |
| 9.1 | `onboarding-vlan`, `mac-iot-174`, `nac-iot-174`, `nac-iot-addr-174`, `fsw-users-net-174`, P3 `P3-nac-174`; `port2` in NAC mode; network monitoring on S3 | All removed; NAC settings and network monitoring at their recorded values |
| 9.2 | `vlp-iot-174`, `dpp-174`; `switch-controller-dynamic` on the FortiLink interface; `port2` dynamic | All removed |
| 9.3 | Quarantine entry `qtn-174`; `bounce-quarantined-link` briefly; `mab-174` on `port2` (Part F) | Entry deleted; globals at their recorded values; `port2` without a security policy |
| 9.4 | IGMP snooping, proxy, and querier on `fsw-users`; per-switch override; flood options; `port2` in `fsw-users` | All removed; `port2` back in `fsw-iot` |

Each lab is self-contained and returns the controller, `FSW-A`, and the
endpoints to the state Chapter 08 left (ADDENDUM 8). On S3 the VLAN-level
settings reach `FSW-B` too; only `FSW-A`'s ports are used.

### What to keep after this chapter

Nothing. The 802.1X objects of Chapter 07 stay as they were, attached to no
port; the endpoints gain only the `iperf` and (optionally) `lldpd` packages.

## Implementation and Automation

The labs are the implementation. Four habits make them traceable.

**Wait for the engines.** The NAC and dynamic port policy engines run every 60
seconds by default, so a match can take up to a minute after the event. Read
the intervals instead of shortening them:

```text
FGT # get switch-controller system
```

**Read both sides.** The controller shows what it matched; the switch shows
what it enforces:

```text
FGT # diagnose switch-controller mac-device nac known
FSW # execute switch-controller get-nac-mac-cache
```

**Watch the endpoint's address and IGMP.** During the quarantine and
multicast labs keep a second window on endpoint A:

```bash
# endpoint A
watch -n 2 ip -br addr show <IFACE>
sudo tcpdump -ni <IFACE> igmp
```

**Make multicast without a media server.** `iperf` (version 2) sends UDP to a
multicast group (`-u`, `-T` sets the TTL, `-B` the source address), and the
`autojoin` flag of `ip address add` makes the Linux kernel join a group and send
the IGMP report that a snooping switch needs; `ip maddr add` alone does not
(`ip-address(8)`):

```bash
# endpoint B (sender)
iperf -c 233.252.0.174 -u -T 1 -B 10.174.41.20 -b 100K -t 30
# endpoint A (receiver)
sudo ip address add 233.252.0.174/32 dev <IFACE> autojoin
```

The FortiOS configuration commands in this chapter were checked against the
FortiOS 7.6.0 CLI Reference. `execute`, `diagnose`, and `get` commands were
checked against the FortiLink Guide 7.6.7 where it prints them (`diagnose user
device list`, `diagnose switch-controller mac-device dynamic`, `mac-device nac
known`, `mac-device nac onboarding`, `mac-device cache`, `diagnose firewall
dynamic list`, `diagnose switch-controller telemetry show mac-stats`,
`diagnose switch-controller switch-info 802.1X`, `show user quarantine`) and
otherwise against the FortiOS 8.0.1 CLI Reference as a cross-check
(`diagnose switch-controller switch-info igmp-snooping group`,
`execute dhcp lease-list`); each is marked where it is used. Switch commands
were checked against the FortiSwitchOS 7.6.7 CLI Reference, with these matched
by hand: `diagnose switch 802-1x status <port>` (an optional port argument,
p. 346), `get switch lldp neighbors-summary` (one alternative of a syntax line
that the verifier cannot expand, p. 499), and `show switch interface` and `show
switch vlan`, which are the `show` forms of documented
`config` tables (the guide prints `show switch vlan 4093` and `show switch
interface port17`, pp. 267–268). The endpoint commands follow `iperf(1)`
(version 2), `ip-address(8)`, `tcpdump(8)`, `lldpcli(8)`, `curl(1)`, and
`ping(8)`.

## Validation and Troubleshooting

| Symptom | Likely cause | Check |
| --- | --- | --- |
| A NAC port's device never leaves `nac onboarding` | No enabled NAC policy matches (a typo in the MAC address, wrong `switch-fortilink`), or the engine has not run yet | `show user nac-policy`; wait 60 s; `diagnose switch-controller mac-device nac known` |
| The device matched but stays in VLAN 4089 | The MAC policy names a VLAN of another FortiLink interface, or no MAC policy is set | `show switch-controller mac-policy`; `execute switch-controller get-nac-mac-cache` on the switch |
| Unmatched devices go nowhere instead of to onboarding | `onboarding-vlan` is empty (the guide's default) | `show switch-controller fortilink-settings` |
| A NAC policy is refused | The NAC settings entry does not exist (no switch discovered yet, Track 2) | Create the entry first (p. 183) |
| The dynamic address is empty | The device has not matched, or `firewall-address` is not set in the NAC policy | `diagnose firewall dynamic list` |
| A DPP never matches | `switch-controller-dynamic` is not set on the FortiLink interface, the port is not `access-mode dynamic`, or the vendor string differs from the device list | `show system interface port3`; `diagnose user device list` |
| The DPP rule matched but the port is unchanged | The VLAN policy, LLDP profile, or QoS policy belongs to another FortiLink interface | `show switch-controller vlan-policy` |
| A quarantined host still reaches the network | `quarantine disable`, or by-redirect mode | `get user quarantine`; `get switch-controller global` |
| A quarantined host is unreachable even in VLAN 4093 | `drop enable`, the port does not allow `quarantine`, or the host kept its old address | `show user quarantine`; `show switch-controller managed-switch`; enable `bounce-quarantined-link` |
| Multicast still reaches a port with snooping on | `flood-unknown-multicast` or `mcast-snooping-flood-traffic` is enabled, a 239.x group on an FS-124F, or the port is an mRouter port | `get switch igmp-snooping group` on the switch |
| A joined receiver stops after about 5 minutes | No querier, so the group aged out | Enable the proxy and the querier (Lab 9.4) |
| `switch-controller-igmp-snooping` is refused on a sixth VLAN | S1 or S2: note 23 | `get switch igmp-snooping status` |

## Security and Best Practices

- **Start NAC with an onboarding VLAN that goes nowhere.** Give unknown devices
  a VLAN with no route to anything sensitive, and let NAC policies move known
  devices out of it; keep the most specific policies first.
- **Match on what cannot be spoofed easily, and know what can.** A MAC address,
  vendor, or operating system is an identification, not an authentication; use
  802.1X (Chapter 07) where a device can authenticate, and NAC where it cannot.
- **Use NAC dynamic addresses in firewall policies.** They keep policy tied to
  device identity instead of to addresses that DHCP reassigns.
- **Make the last DPP rule the safe default.** A port whose device matches no
  rule should end up in a restricted VLAN, not in a user VLAN.
- **Keep the quarantine VLAN on every host port.** Without `quarantine` in the
  allowed and untagged lists, quarantine-by-VLAN cannot move a host there.
- **Enable `bounce-quarantined-link` for DHCP clients.** Otherwise a quarantined
  host keeps an address that no longer works and never reaches the quarantine
  portal.
- **Run IGMP snooping with a querier.** Without one, groups age out and
  receivers lose streams; on S1 and S2 spend the five snooping VLANs on the
  VLANs that carry multicast.

## References and Knowledge Checks

**References**

- [Fortinet, *FortiLink Guide (FortiOS 7.6.7)*](https://docs.fortinet.com/document/fortiswitch/7.6.7/fortilink-guide)
  — MCLAG and IGMP snooping (p. 85), IGMP-snooping settings, proxy, and querier
  (pp. 146–149), device detection, voice device detection, and IoT detection
  (pp. 164–172), FortiSwitch NAC, NAC settings, NAC policies, MAC policies,
  viewing matched devices, device statistics, and LAN segments (pp. 182–210),
  dynamic port policies and VLAN policies (pp. 211–216), NAC with 802.1X
  (pp. 233–234), quarantines (pp. 263–272).
- [Fortinet, *FortiSwitchOS 7.6.7 Administration Guide (Standalone Mode)*](https://docs.fortinet.com/document/fortiswitch/7.6.7/administration-guide)
  — MCLAG with IGMP snooping (p. 172), DHCP snooping, ARP inspection, and access
  VLAN together from 7.6.5 (p. 276), IGMP snooping (pp. 312–318).
- [Fortinet, *FortiSwitchOS 7.6.7 CLI Reference*](https://docs.fortinet.com/document/fortiswitch/7.6.7/fortiswitchos-cli-reference)
  — `config switch global` (`mclag-igmpsnooping-aware`, p. 118), `config switch
  igmp-snooping globals` (p. 125), `config switch vlan` (pp. 185–186),
  `diagnose switch 802-1x status` (p. 346), `diagnose switch mac-address`
  (p. 354), `diagnose switch vlan assignment` (p. 382), `execute
  switch-controller get-nac-mac-cache` (p. 451), `get switch igmp-snooping`
  (pp. 496–497), `get switch lldp` (p. 499).
- [Fortinet, FortiOS 7.6 documentation](https://docs.fortinet.com/product/fortigate/7.6)
  — the FortiOS 7.6.0 CLI Reference: `config user nac-policy`, `config user
  quarantine`, `config switch-controller quarantine`, `config switch-controller
  mac-policy`, `dynamic-port-policy`, `vlan-policy`, `fortilink-settings`,
  `system`, `global`, `network-monitor-settings`, `igmp-snooping`,
  `traffic-policy`, `config switch-controller managed-switch` (`ports`,
  `igmp-snooping`, `mclag-igmp-snooping-aware`), `config system interface`
  (`switch-controller-igmp-snooping*`, `switch-controller-dynamic`,
  `switch-controller-iot-scanning`), `config firewall address` (`sub-type
  swc-tag`).
- FortiOS 8.0.1 CLI Reference (cross-check only) — `diagnose switch-controller
  switch-info igmp-snooping`, `diagnose switch-controller mac-device`, `execute
  dhcp lease-list`.
- FortiSwitchOS 7.6.7 feature matrix (`temp/fsw/FSW-7.6.7-Feature-Matrix.pdf`)
  — the FortiGate integration, NAC, multicast, and MCLAG rows; notes 12 and 23.
- [RFC 5771](https://www.rfc-editor.org/rfc/rfc5771) — IPv4 multicast address
  assignments, including `233.252.0.0/24` for documentation.
- [`iperf(1)`](https://manpages.ubuntu.com/manpages/noble/man1/iperf.1.html),
  [`ip-address(8)`](https://manpages.ubuntu.com/manpages/noble/man8/ip-address.8.html)
  (`autojoin`), [`lldpcli(8)`](https://manpages.ubuntu.com/manpages/noble/man8/lldpcli.8.html),
  [`tcpdump(8)`](https://manpages.ubuntu.com/manpages/noble/man8/tcpdump.8.html).

**Knowledge checks**

1. Which three sources feed the FortiGate's device list for devices behind a
   managed switch, and which of them is a dash on the FS-108F and FS-124F?
2. Where does a device on a NAC-mode port go before it matches a policy, and
   which object decides where it goes after it matches?
3. What does a NAC policy's dynamic firewall address contain, and how does a
   firewall policy use it?
4. Name two reasons NAC LAN segments are read-and-predict in this volume, one
   of them specific to the FS-108F.
5. How does a dynamic port policy differ from a NAC policy in what it changes?
6. In quarantine-by-VLAN mode, what does the switch receive from the
   controller, and why must every host port allow the quarantine VLAN?
7. Why does a quarantined DHCP client need `bounce-quarantined-link`, and what
   does `drop enable` change?
8. What happens to a joined multicast group on a VLAN with IGMP snooping but no
   querier, and what must be enabled before the switch's querier?
9. Why does this lab avoid 239.x.x.x groups on the FS-124F, and how many VLANs
   can run IGMP snooping on S1 and S2?
10. Why is MLD snooping read-and-predict on every switch option?

## Hands-On Lab

**Shared prerequisites.** Chapter 08 complete (ADDENDUM 8 state):
`<SWITCH_SN>` `Authorized/Up` at `10.255.1.2` with profile `fsw-174-prof` (on
S3, `FSW-A`; `FSW-B` managed and in the MCLAG of Chapter 06); `port1` native
`fsw-users` (endpoint A, DHCP, `discard-mode none`) and `port2` native `fsw-iot`
(endpoint B, `10.174.43.20/24`), both with BPDU guard, no security policy, and
`quarantine` in their allowed lists; P1 and P2 as Chapter 04 left them, and on
C2 P3 free. The 802.1X objects `dot1x-174`, `dot1x-174-port`, and `mab-174`
exist, and FreeRADIUS holds endpoint B's MAB entry (Chapter 07). Endpoints A
and B have `tcpdump`; install `iperf` on endpoint B for Lab 9.4 (`sudo apt
install -y iperf`). Track 2: the Lab 2.2 pre-provisioning outcome and the
stand-in entry `S248EPTF18000000` if that outcome allowed it. **Cost:** none.

`FGT #` is the controller on any option. `<SWITCH_SN>` is your switch's serial
number (on Track 2, `S248EPTF18000000`). `<IFACE>` and `<IFACE_B>` are endpoint
A's and endpoint B's wired interfaces, and `<MAC_A>` and `<MAC_B>` their MAC
addresses in the colon form `ip -br link` prints (Lab 2.5). `port3` is the
FortiLink interface on C2 (see Design Considerations for C1 and C3). Before the
first change, back up the controller:

```text
FGT # execute backup config tftp fgt-pre-9-1-174.conf 10.30.99.50
```

### Lab 9.1 — Device detection and a NAC policy

**Objective:** Read what the controller knows about endpoint B, prepare the
NAC settings, put `port2` in NAC mode, watch endpoint B wait in the onboarding
VLAN and then move to `fsw-iot` when a NAC policy matches its MAC address, and
let only the matched device reach `fsw-users` through P3 and the policy's
dynamic firewall address; predict NAC LAN segments.

**Platform notes:** Hands-on on C1 and C3 (and C2 when Lab 4.1's lab VLANs
were a GO) with S1, S2, or S3 (on S3, `FSW-A`): device detection, NAC, and host
quarantine are chain in both columns. Network device detection (step 2) is
hands-on only on S3 (dash in 1xxE/1xxF); NAC device telemetry (step 9) only on
S3, and the guide's list omits the plain FS-248E. On C2, Part C uses P3 and
deletes it. Part D (LAN segments) is read-and-predict on every option. FortiGuard
IoT detection needs a license that C2 lacks; it is read only. Track 2: the NAC
settings, MAC and NAC policies, address objects, and P3 run live; the port step
runs on the stand-in only with Lab 2.2's third outcome; device matching is
read-and-predict.

**Track 1, Part A — what the controller knows:**

1. Read the device sources and the device list. Start a ping from endpoint B so
   that the FortiGate sees its traffic:

   ```bash
   # endpoint B
   ping -c 5 10.174.43.1
   ```

   ```text
   FGT # get switch-controller global
   FGT # diagnose user device list
   ```

   In the `get` output, record `update-user-device` (the 7.6.0 default lists
   `mac-cache lldp dhcp-snooping l2-db l3-db`). In the device list, find
   `<MAC_B>` and record the fields the controller shows for it, in particular
   the hardware vendor, as `<B_VENDOR>` (empty is a valid result). Predict
   whether a vendor appears. **Answer:** the documentation does not say what
   FortiOS derives for a Linux endpoint; record what happens. Lab 9.2 uses
   `<B_VENDOR>` if it is not empty.

2. Read network-assisted device detection and, on S3, turn it on:

   ```text
   FGT # get switch-controller network-monitor-settings
   FGT # config switch-controller network-monitor-settings
   set network-monitoring enable
   end
   ```

   Record the starting value (7.6.0 default `disable`). On S1 and S2 the matrix
   marks network device detection as not supported; record whether FortiOS
   accepts the setting and whether `diagnose user device list` changes. Set it
   back to the recorded value in the rollback.

3. Read the FortiGuard IoT settings without changing them:

   ```text
   FGT # get switch-controller system
   FGT # show system interface port3
   ```

   Record `iot-scan-interval`, `iot-holdoff`, `iot-mac-idle`,
   `iot-weight-threshold`, and `nac-periodic-interval` (60). A missing
   `switch-controller-iot-scanning` line means `disable`, the default (p. 171).

**Track 1, Part B — NAC settings, policy, and port:**

4. Read the NAC settings and the onboarding VLAN:

   ```text
   FGT # show switch-controller fortilink-settings
   FGT # show system interface onboarding
   ```

   Record the entry name as `<FL_SETTINGS>` and its `onboarding-vlan`,
   `inactive-timer`, and `link-down-flush`. Predict the entry name. **Answer:**
   the FortiLink interface's name (`port3` on C2): the controller creates it
   when the first switch is discovered (p. 183). Predict `onboarding-vlan`.
   **Answer:** the guide says none is assigned by default (p. 184); record
   yours. The `onboarding` interface should show `vlanid 4089` and
   `switch-controller-feature nac`, with no address (Chapter 03).

5. Set the onboarding VLAN (skip this if it is already `onboarding`):

   ```text
   FGT # config switch-controller fortilink-settings
   edit <FL_SETTINGS>
   config nac-ports
   set onboarding-vlan "onboarding"
   end
   next
   end
   ```

6. Create the MAC policy (the action) and the NAC policy (the match). The MAC
   policy keeps the 7.6.0 default `bounce-port-link enable`; endpoint B has a
   static address, so a bounce costs it nothing:

   ```text
   FGT # config switch-controller mac-policy
   edit "mac-iot-174"
   set description "Lab 9.1 assign fsw-iot"
   set fortilink "port3"
   set vlan "fsw-iot"
   next
   end
   FGT # config user nac-policy
   edit "nac-iot-174"
   set description "Lab 9.1 endpoint B"
   set category device
   set status enable
   set mac <MAC_B>
   set switch-fortilink "port3"
   set switch-mac-policy "mac-iot-174"
   next
   end
   ```

7. Record `port2` as it is, then put it in NAC mode. Start a continuous ping on
   endpoint B first:

   ```bash
   # endpoint B
   ping 10.174.43.1
   ```

   ```text
   FGT # show switch-controller managed-switch <SWITCH_SN>
   FGT # config switch-controller managed-switch
   edit <SWITCH_SN>
   config ports
   edit "port2"
   set access-mode nac
   next
   end
   next
   end
   ```

   Record `port2`'s `vlan`, `allowed-vlans`, and `untagged-vlans` from the
   `show` before the change. Predict the ping over the next two minutes.
   **Answer:** a gap. Changing to NAC mode bounces the port by default (p. 184),
   and endpoint B's MAC address is a new NAC device that starts in the
   onboarding VLAN, which has no gateway; within one NAC engine run (60 s) it
   matches `nac-iot-174` and the MAC policy puts it in `fsw-iot`, and the ping
   resumes. Record how long the gap was.

8. Read the result on both sides:

   ```text
   FGT # diagnose switch-controller mac-device nac known
   FGT # diagnose switch-controller mac-device nac onboarding
   FGT # diagnose switch-controller mac-device cache
   FSW # execute switch-controller get-nac-mac-cache
   FSW # show switch interface port2
   FGT # show switch-controller managed-switch <SWITCH_SN>
   ```

   Predict where `<MAC_B>` appears. **Answer:** in `nac known` with
   `MATCHED-NAC-POLICY nac-iot-174` and `MAC-POLICY-ACTION mac-iot-174`, last
   switch `<SWITCH_SN>`, last port `port2`; not in `nac onboarding`; the switch's
   NAC cache shows it with VLAN 1743. Record whether the cache still shows an
   earlier line with VLAN 4089, what `show switch interface port2` prints for
   the native VLAN, and whether FortiOS changed `port2`'s `vlan` or VLAN lists
   in its own configuration (the documentation does not say; record what
   happens).

9. On S3, count the device's traffic (NAC device telemetry; skip on S1 and S2,
   where the matrix marks it unsupported):

   ```text
   FGT # config switch-controller mac-policy
   edit "mac-iot-174"
   set count enable
   next
   end
   FGT # diagnose switch-controller telemetry show mac-stats
   ```

   After a minute of ping, `<MAC_B>` should show growing receive counters; only
   receive counters are reported, and the guide warns that accuracy is not
   guaranteed (p. 205). On an FS-248E pair (not in the guide's list), record
   whether the entry appears at all.

**Track 1, Part C — the dynamic firewall address and P3:**

10. Create the dynamic address and attach it to the NAC policy:

    ```text
    FGT # config firewall address
    edit "nac-iot-addr-174"
    set type dynamic
    set sub-type swc-tag
    next
    end
    FGT # config user nac-policy
    edit "nac-iot-174"
    set firewall-address "nac-iot-addr-174"
    next
    end
    FGT # diagnose firewall dynamic list
    ```

    Within a NAC engine run, `nac-iot-addr-174` should list `<MAC_B>`
    (pp. 191, 194).

11. Record endpoint A's current address (`ip -br addr show <IFACE>`) as
    `<LEASE_A>`, then test from endpoint B:

    ```bash
    # endpoint B
    ping -c 3 <LEASE_A>
    ```

    Predict. **Answer:** it fails. `fsw-iot` and `fsw-users` are both in
    `FSW-LAN`, whose `intrazone deny` blocks traffic between member interfaces,
    and no policy allows it.

12. Allow ping from whatever matched `nac-iot-174` to `fsw-users`, with P3. The
    policy names the zone, because its members are configured through it
    (FortiOS 7.6.0 CLI Reference, `config system zone`), and the address
    objects narrow it:

    ```text
    FGT # config firewall address
    edit "fsw-users-net-174"
    set subnet 10.174.41.0 255.255.255.0
    next
    end
    FGT # config firewall policy
    edit 0
    set name "P3-nac-174"
    set srcintf "FSW-LAN"
    set dstintf "FSW-LAN"
    set srcaddr "nac-iot-addr-174"
    set dstaddr "fsw-users-net-174"
    set action accept
    set schedule "always"
    set service "PING"
    set logtraffic all
    next
    end
    FGT # show firewall policy
    ```

    Record the new policy's ID as `<P3_ID>`. Repeat step 11's ping: it works.
    Then ping endpoint B from endpoint A (`ping -c 3 10.174.43.20`): it fails,
    because P3 has the NAC address only as its source.

**Track 1, Part D — NAC LAN segments (read-and-predict):**

13. The guide's LAN segment example (pp. 206–210) adds two VLANs without
    addresses to the segment and places ports in NAC mode, trimmed:

    ```text
    config switch-controller fortilink-settings
    edit "fortilink"
    config nac-ports
    set onboarding-vlan "onboarding"
    set lan-segment enabled
    set nac-lan-interface "nac_segment"
    set nac-segment-vlans "voice" "video" "Office2" "Office1"
    end
    next
    end
    config switch-controller managed-switch
    edit "S248EPTF18001384"
    config ports
    edit "port1"
    set vlan "onboarding"
    set allowed-vlans "quarantine" "nac_segment"
    set untagged-vlans "quarantine" "nac_segment"
    set access-mode nac
    next
    end
    next
    end
    ```

    Predict three things. (a) Which address does a device in `Office1` get?
    **Answer:** one from the `nac_segment` DHCP server (`10.255.13.0/24` in the
    guide), the primary interface whose address and DHCP server the segment
    VLANs share; moving between segment VLANs does not change it. (b) Could this
    lab add `fsw-iot` to `nac-segment-vlans`? **Answer:** not as built: segment
    VLANs must have no address, `allowaccess`, or DHCP server (p. 186), and
    `fsw-iot` has an address and is in `FSW-LAN`. (c) Could S1 run it?
    **Answer:** not as cabled: note 12 says the FS-108F family cannot be directly
    connected to a FortiGate with LAN segments, and S1 is.

**Track 2:** Run steps 3 to 6 and 10 to 12's controller blocks on your
controller (on FGT-1 alone P3 is free unless Lab 4.1 used it). If step 4
shows no NAC settings entry (a controller that has never discovered a switch),
create it first and delete it in the rollback:

```text
FGT # config switch-controller fortilink-settings
edit "port3"
set fortilink "port3"
next
end
```

Record whether `show system interface onboarding` finds an interface (it does
not exist until a switch has been discovered, Chapter 03); if it does not, use
`onboarding-vlan` with any existing FortiSwitch VLAN or skip step 5. If Lab 2.2's
third outcome applies, run step 7's port block against `S248EPTF18000000`. Check
the objects with `show user nac-policy`, `show switch-controller mac-policy`,
and `show firewall policy <P3_ID>`. Skip the endpoint and switch steps.

**Track 2: read-and-predict.**

1. The guide prints this `nac known` output (p. 203), trimmed:

   ```text
   MAC               LAST-KNOWN-SWITCH LAST-KNOWN-PORT MATCHED-NAC-POLICY MAC-POLICY-ACTION LAST-SEEN(sec) OVERRIDE(min) FSW-ID COMMENTS
   0c:82:b9:ae:00:00 S548DF4K15000008  port5           ems                ems               0              -             2      auto detected @ 2024-08-16 00:12:39
   Matched Devices in the vdom:2 (All-vdom:2 Max:14400)
   ```

   Predict what `Max:14400` means on that FortiGate. **Answer:** the most known
   NAC devices it supports, 48 times its maximum number of managed switches
   (p. 188), so that model manages 300 switches.
2. The guide's `mac-device cache` output (p. 204) lists some devices in VLAN
   4089 and others in VLANs 103 and 104. Predict which ones are in
   `nac onboarding`. **Answer:** the VLAN 4089 devices: 4089 is the onboarding
   VLAN, where unmatched NAC devices wait.
3. A NAC policy is disabled while its device is connected. Predict.
   **Answer:** at the next engine run the device no longer matches and returns
   to the onboarding VLAN (the negative test below checks this live).

**Expected result:** Track 1: you recorded `update-user-device`, endpoint B's
device-list entry and `<B_VENDOR>`, and network monitoring's behavior on your
switch; `port2` in NAC mode briefly put endpoint B in VLAN 4089, then
`nac-iot-174` moved it to `fsw-iot`, visible in `nac known` and in the switch's
NAC cache; on S3 telemetry counted its packets; the dynamic address held
`<MAC_B>`, and P3 let endpoint B, and only in that direction, ping endpoint A;
the LAN segment predictions are answered. Track 2: the objects exist and the
predictions are answered.

**Negative test:** Disable the NAC policy and watch endpoint B's ping:

```text
FGT # config user nac-policy
edit "nac-iot-174"
set status disable
next
end
```

Predict and observe: within about a minute endpoint B's ping to `10.174.43.1`
stops, `<MAC_B>` moves from `nac known` to `nac onboarding`, and `diagnose
firewall dynamic list` no longer lists it in `nac-iot-addr-174`. Set `status
enable` again and record how long recovery takes. Track 2: prediction 3 is the
negative test.

**Rollback:** Remove the policy and addresses first, then the NAC objects,
then restore the port, the onboarding VLAN, and network monitoring to the
values you recorded (shown here as no onboarding VLAN and the 7.6.0 default
`disable`):

```text
FGT # config firewall policy
delete <P3_ID>
end
FGT # config user nac-policy
delete "nac-iot-174"
end
FGT # config firewall address
delete "nac-iot-addr-174"
delete "fsw-users-net-174"
end
FGT # config switch-controller managed-switch
edit <SWITCH_SN>
config ports
edit "port2"
set access-mode static
set vlan "fsw-iot"
next
end
next
end
FGT # config switch-controller mac-policy
delete "mac-iot-174"
end
FGT # config switch-controller fortilink-settings
edit <FL_SETTINGS>
config nac-ports
unset onboarding-vlan
end
next
end
FGT # config switch-controller network-monitor-settings
set network-monitoring disable
end
```

If step 7's `show` differed from the recorded lists afterwards, put
`quarantine` back with `append allowed-vlans "quarantine"` and `append
untagged-vlans "quarantine"` under `port2`. Confirm that endpoint B reaches
`10.174.43.1`, that `show firewall policy` lists only P1 and P2 (on C2, P3 is
free again), and that `show switch-controller managed-switch <SWITCH_SN>` shows
`port2` as Chapter 08 left it.

**Lab verified by:** *pending*

### Lab 9.2 — Dynamic port policies with VLAN, LLDP, and QoS actions

**Objective:** Build a VLAN policy and a dynamic port policy whose rule
matches endpoint B, first by MAC address and then by hardware vendor, and
applies the VLAN policy, an LLDP profile, and a QoS policy to `port2`; read
the match on the controller and the result on the switch.

**Platform notes:** Hands-on on C1 and C3 (and C2 with a lab-VLAN GO) with S1,
S2, or S3 (on S3, `FSW-A`): dynamic port policies are chain in both columns.
The vendor match (step 7) depends on Lab 9.1's `<B_VENDOR>`; the LLDP step (8)
is optional and needs the `lldpd` package on endpoint B. An LLDP-MED phone is
Chapter 10's subject. Track 2: the VLAN policy, the DPP, and the FortiLink
interface setting run live; the port step runs on the stand-in only with Lab
2.2's third outcome; matching is read-and-predict.

**Track 1:**

1. Find the LLDP profiles and QoS policies that already exist:

   ```text
   FGT # show switch-controller lldp-profile
   FGT # show switch-controller qos qos-policy
   ```

   The guide calls `fortivoice.fortilink` and `voice-qos` predefined (p. 164);
   record whether your controller has them. If either is missing, leave its
   line out of step 3 and record that.

2. Create the VLAN policy. It keeps `quarantine` allowed and untagged, as every
   host port must:

   ```text
   FGT # config switch-controller vlan-policy
   edit "vlp-iot-174"
   set description "Lab 9.2 fsw-iot access"
   set fortilink "port3"
   set vlan "fsw-iot"
   set allowed-vlans "quarantine"
   set untagged-vlans "quarantine"
   next
   end
   ```

3. Create the dynamic port policy with one rule that matches endpoint B's MAC
   address:

   ```text
   FGT # config switch-controller dynamic-port-policy
   edit "dpp-174"
   set description "Lab 9.2"
   set fortilink "port3"
   config policy
   edit "ep-b-174"
   set description "endpoint B"
   set status enable
   set category device
   set mac <MAC_B>
   set vlan-policy "vlp-iot-174"
   set lldp-profile "fortivoice.fortilink"
   set qos-policy "voice-qos"
   next
   end
   next
   end
   ```

4. Turn dynamic port policies on for the FortiLink interface. Record the
   current value first (a missing line means none):

   ```text
   FGT # show system interface port3
   FGT # config system interface
   edit "port3"
   set switch-controller-dynamic <FL_SETTINGS>
   next
   end
   ```

5. Start a continuous ping on endpoint B, then make `port2` a dynamic port:

   ```text
   FGT # config switch-controller managed-switch
   edit <SWITCH_SN>
   config ports
   edit "port2"
   set access-mode dynamic
   set port-policy "dpp-174"
   next
   end
   next
   end
   ```

6. Wait up to a minute (`dynamic-periodic-interval`), then read the match and
   the port:

   ```text
   FGT # diagnose switch-controller mac-device dynamic
   FGT # show switch-controller managed-switch <SWITCH_SN>
   FSW # show switch interface port2
   ```

   Predict the `mac-device dynamic` line. **Answer:** `<MAC_B>`, your switch,
   `port2`, dynamic port policy `dpp-174`, policy `ep-b-174` (the guide's
   example shows the same columns, p. 171). `port2` shows `matched-dpp-policy`
   with the rule, and on the switch its native VLAN is 1743 with the
   profile and QoS policy applied. Record the gap in the ping: the rule's
   `bounce-port-link` defaults to `enable`.

7. Match by vendor instead of MAC address (skip if `<B_VENDOR>` was empty in
   Lab 9.1). The value must be the string the device list shows, at most 15
   characters:

   ```text
   FGT # config switch-controller dynamic-port-policy
   edit "dpp-174"
   config policy
   edit "ep-b-174"
   unset mac
   set hw-vendor "<B_VENDOR>"
   next
   end
   next
   end
   ```

   Bounce endpoint B's link (`sudo ip link set <IFACE_B> down && sudo ip link
   set <IFACE_B> up`) and repeat step 6. Record whether the rule still matches;
   the documentation lists the matchable values (p. 211) but not how FortiOS
   identifies a Linux endpoint.

8. Optional, LLDP from the endpoint. Install and start `lldpd` on endpoint B,
   then read the neighbor on both sides:

   ```bash
   # endpoint B
   sudo apt install -y lldpd
   sudo lldpcli show neighbors
   ```

   ```text
   FSW # get switch lldp neighbors-summary
   FGT # diagnose user device list
   ```

   The switch lists endpoint B's system name on `port2`. Record whether the controller's device entry for
   `<MAC_B>` now shows that host name: `update-user-device` includes `lldp`,
   but the guide documents LLDP-based detection only for voice devices
   (p. 164). Stop `lldpd` afterwards (`sudo systemctl disable --now lldpd`).

**Track 2:** Run steps 1 to 4 on your controller. If Lab 2.2's third outcome
applies, run step 5 against `S248EPTF18000000`. Check with `show
switch-controller dynamic-port-policy` and `show switch-controller vlan-policy`.

**Track 2: read-and-predict.**

1. The guide's voice example (pp. 170–171) applies a dynamic port policy to
   `port2` and prints:

   ```text
   MAC               LAST-KNOWN-SWITCH LAST-KNOWN-PORT DYNAMIC-PORT-POLICY POLICY    LAST-SEEN COMMENTS
   00:15:65:83:cb:16 S108DVIJAK1VGG54  port2           FortiFone           FortiFone 148       auto detected @ 2021-04-29 19:12:42
   ```

   Predict how the switch learned that this device is a FortiFone. **Answer:**
   from its LLDP messages, which FortiSwitchOS parses and passes to the
   FortiGate (p. 164); the rule matched `family "FortiFone"`.
2. A DPP has two rules, a MAC-address rule for a printer and a last rule with a
   VLAN policy for a guest VLAN. A laptop is plugged into the port. Predict.
   **Answer:** the laptop matches no specific rule; the last rule is meant to
   hold the default properties (p. 211), and whether a rule with no match
   fields matches everything is not documented, so record what happens if you
   build it.
3. Predict what `set 802-1x "mab-174"` in a rule would do. **Answer:** apply
   that 802.1X security policy to the port when the rule matches (p. 214).

**Expected result:** Track 1: the existing LLDP profiles and QoS policies are
recorded; `dpp-174` matched endpoint B by MAC address within a minute and
`port2` took VLAN 1743 with the LLDP profile and QoS policy; the vendor match
and the LLDP neighbor test are recorded. Track 2: the objects exist and the
predictions are answered.

**Negative test:** Point the rule at a MAC address that is not on the port
(the locally administered `02:00:00:00:01:74`), then bounce endpoint B's link:

```text
FGT # config switch-controller dynamic-port-policy
edit "dpp-174"
config policy
edit "ep-b-174"
unset hw-vendor
set mac 02:00:00:00:01:74
next
end
next
end
```

Predict and observe: after a minute `diagnose switch-controller mac-device
dynamic` no longer lists `<MAC_B>`, and `matched-dpp-policy` is empty. The guide
does not say which VLAN an unmatched dynamic port falls back to; record `show
switch interface port2` and whether endpoint B's ping works. Track 2:
prediction 2 is the negative test.

**Rollback:** Put the port back first, then remove the FortiLink setting (or
restore the value recorded in step 4) and the policies:

```text
FGT # config switch-controller managed-switch
edit <SWITCH_SN>
config ports
edit "port2"
set access-mode static
unset port-policy
set vlan "fsw-iot"
next
end
next
end
FGT # config system interface
edit "port3"
unset switch-controller-dynamic
next
end
FGT # config switch-controller dynamic-port-policy
delete "dpp-174"
end
FGT # config switch-controller vlan-policy
delete "vlp-iot-174"
end
```

Check `port2` with `show switch-controller managed-switch <SWITCH_SN>`; if
`quarantine` is missing from its lists, `append` it as in Lab 9.1. Confirm that
endpoint B reaches `10.174.43.1`, and on endpoint B remove `lldpd` if you
installed it (`sudo apt remove -y lldpd`).

**Lab verified by:** *pending*

### Lab 9.3 — Quarantine a host

**Objective:** Read the quarantine settings and the quarantine VLAN, quarantine
endpoint A by MAC address, see it move to VLAN 4093 and then to the quarantine
DHCP server, release it, repeat with `bounce-quarantined-link` and with `drop`,
read a quarantined 802.1X MAC-based session, and predict quarantine-by-redirect.

**Platform notes:** Hands-on on C1, C2, and C3 with S1, S2, or S3 (on S3,
`FSW-A`): host quarantine is chain in both columns, and no interface or policy
is added, so C2 runs it in full even after a lab-VLAN NO-GO if `port1` has a
native VLAN with DHCP (otherwise use C1 or C3). Part F needs Chapter 07's
`mab-174` and FreeRADIUS. Part G (by-redirect) is read-and-predict on every
option. Track 2: the quarantine entry and global settings run live with no
switch to act on; the switch and endpoint steps are read-and-predict.

**Track 1, Part A — the starting state:**

1. Read the controller side:

   ```text
   FGT # get user quarantine
   FGT # get switch-controller global
   FGT # show system interface quarantine
   FGT # show system dhcp server
   FGT # show switch-controller managed-switch <SWITCH_SN>
   ```

   Record `quarantine` (7.6.0 default `enable`), `quarantine-mode`
   (`by-vlan`), and `bounce-quarantined-link` (`disable`). The `quarantine`
   interface should show `10.255.11.1/24`, `switch-controller-access-vlan
   enable`, `security-mode captive-portal`, and `vlanid 4093`; if your
   controller instead has `qtn.<port>` with `10.254.254.254` (the guide's
   quarantine pages, p. 270), use that name below. Find the DHCP server whose
   `interface` is the quarantine interface. Confirm that `port1` lists
   `quarantine` in `allowed-vlans` and `untagged-vlans` and has `discard-mode
   none` (Lab 8.5's rollback).

2. Read the switch side:

   ```text
   FSW # show switch vlan 4093
   ```

   Record `description`, `access-vlan`, and whether `dhcp-snooping` appears.
   The guide's example shows both `dhcp-snooping enable` and `access-vlan
   enable` (p. 268); on a build before FortiSwitchOS 7.6.5 that combination is
   not supported on one VLAN (Administration Guide, p. 276), so record what
   yours shows and do not add DAI or snooping to this VLAN.

**Track 1, Part B — quarantine endpoint A:**

3. On endpoint A, start a continuous ping to `10.174.41.1` and the address
   watch (Implementation and Automation). Then quarantine `<MAC_A>`:

   ```text
   FGT # config user quarantine
   config targets
   edit "qtn-174"
   set description "Lab 9.3 endpoint A"
   config macs
   edit <MAC_A>
   set drop disable
   next
   end
   next
   end
   end
   ```

   Predict endpoint A's ping and address. **Answer:** the ping stops: the switch
   now puts endpoint A's frames in VLAN 4093, where `10.174.41.1` does not
   exist. The address stays in `10.174.41.0/24`, because nothing told the DHCP
   client to renew; that is the problem `bounce-quarantined-link` solves
   (p. 267).

4. Read the binding:

   ```text
   FGT # show user quarantine
   FGT # diagnose switch-controller mac-device cache
   FSW # show switch vlan 4093
   FSW # diagnose switch vlan assignment mac list
   FSW # diagnose switch mac-address list
   ```

   Predict. **Answer:** VLAN 4093 lists `<MAC_A>` under `config member-by-mac`,
   and the VLAN assignment list shows it in VLAN 4093 (pp. 268–269); the MAC
   table shows it on `port1` in VLAN 4093. Record the `Source` line the switch
   prints.

5. Renew endpoint A's address and look at the quarantine network:

   ```bash
   # endpoint A
   sudo ip link set <IFACE> down && sudo ip link set <IFACE> up
   sleep 10; ip -br addr show <IFACE>
   ping -c 3 10.255.11.1
   curl -s -m 5 http://10.255.11.1/ | head -n 5
   ```

   ```text
   FGT # execute dhcp lease-list
   ```

   Endpoint A should lease an address from the quarantine DHCP server
   (`10.255.11.0/24`); the lease list (FortiOS 8.0.1, cross-check) shows it on
   the quarantine interface. Record whether the ping to `10.255.11.1` works
   and what `curl` returns: the interface has `security-mode captive-portal`,
   and the documentation does not show the page a quarantined host gets.

**Track 1, Part C — release:**

6. Release endpoint A and renew:

   ```text
   FGT # config user quarantine
   config targets
   edit "qtn-174"
   config macs
   delete <MAC_A>
   end
   next
   end
   end
   ```

   Bounce endpoint A's link as in step 5. Endpoint A leases from `fsw-users`
   again and its ping to `10.174.41.1` works. `show switch vlan 4093` no longer
   lists `<MAC_A>`.

**Track 1, Part D — bounce the link automatically:**

7. Enable the bounce, quarantine endpoint A again, and watch without touching
   the endpoint:

   ```text
   FGT # config switch-controller global
   set bounce-quarantined-link enable
   end
   FGT # config user quarantine
   config targets
   edit "qtn-174"
   config macs
   edit <MAC_A>
   set drop disable
   next
   end
   next
   end
   end
   ```

   Predict. **Answer:** `port1` goes down and up, and endpoint A's DHCP client
   leases a `10.255.11.0/24` address on its own. Release it as in step 6 without
   bouncing by hand: the port bounces again at release and endpoint A returns to
   `fsw-users` (p. 267). Record both transitions.

**Track 1, Part E — drop:**

8. Quarantine endpoint A with `drop enable` (step 7's block with `set drop
   enable`). Predict. **Answer:** after the bounce endpoint A gets no address at
   all and cannot reach `10.255.11.1`: `enable` blocks the device's traffic
   instead of sending it to the FortiGate (p. 265). Release it as in step 6.

**Track 1, Part F — quarantine with 802.1X MAC-based authentication (optional):**

9. Apply Chapter 07's MAB-only policy to `port2`, check that endpoint B is
   authorized, and quarantine `<MAC_B>`:

   ```text
   FGT # config switch-controller managed-switch
   edit <SWITCH_SN>
   config ports
   edit "port2"
   set port-security-policy "mab-174"
   next
   end
   next
   end
   FGT # diagnose switch-controller switch-info 802.1X <SWITCH_SN> port2
   FGT # config user quarantine
   config targets
   edit "qtn-174"
   config macs
   edit <MAC_B>
   set drop disable
   next
   end
   next
   end
   end
   FGT # diagnose switch-controller switch-info 802.1X <SWITCH_SN> port2
   FSW # diagnose switch 802-1x status port2
   ```

   Predict the second session output. **Answer:** `Quarantine VLAN (4093)
   detection : Enable`, and the client table shows `<MAC_B>` with `4093` in its
   `Quarantined` column, as in the guide's example (pp. 268–269); before the
   quarantine, the dynamic VLAN was 1743 from FreeRADIUS. The switch command's
   port argument is optional (matched by hand). Then delete `<MAC_B>` from
   `qtn-174` as in step 6.

**Track 1, Part G — quarantine-by-redirect (read-and-predict):**

10. The guide's procedure for by-redirect is: disable quarantine, set
    `quarantine-mode by-redirect`, remove the quarantine VLAN from the switch
    ports, and enable quarantine (p. 264). Predict where a quarantined device's
    traffic goes and which firewall object matters. **Answer:** it stays in its
    own VLAN and is redirected to the FortiGate only; firewall policies see it
    through the address group `QuarantinedDevices`, which by-redirect requires.
    This volume does not run it, because removing `quarantine` from the ports
    would break the rule that every host port keeps it.

**Track 2:** Run steps 1, 3, 6, and 7's controller blocks on your controller,
and check with `show user quarantine` and `get switch-controller global`.
Record whether a `quarantine` interface exists (Chapter 03's Track 2 result).
Skip the endpoint and switch steps; Parts F and G are predictions.

**Track 2: read-and-predict.**

1. The guide's switch, after a MAC address is quarantined (p. 268):

   ```text
   config switch vlan
   edit 4093
   set description "qtn.FLNK10"
   set dhcp-snooping enable
   set access-vlan enable
   config member-by-mac
   edit 1
   set mac 00:05:65:ad:15:03
   next
   end
   next
   end
   ```

   Predict how a host with that MAC address can still reach the FortiGate but
   not another host in VLAN 4093. **Answer:** `member-by-mac` puts its frames in
   VLAN 4093 whatever the port's native VLAN; `access-vlan enable` blocks
   host-to-host traffic in that VLAN, so only the FortiGate is reachable
   (Chapter 08).
2. An administrator adds a MAC address to a quarantine entry while `quarantine
   disable` is set. Predict. **Answer:** nothing happens until quarantine is
   enabled; then it is quarantined (p. 264). The negative test checks this.
3. The guide's quarantine example (p. 271) shows ports with
   `allowed-vlans "qtn.port7"` and `untagged-vlans "qtn.port7"`. Predict why
   untagged. **Answer:** quarantined hosts send untagged frames; the quarantine
   VLAN must leave the port untagged for them to receive the replies.

**Expected result:** Track 1: the starting values and the switch's view of
VLAN 4093 are recorded; quarantining endpoint A stopped its traffic, the switch
bound `<MAC_A>` to VLAN 4093, and after a renewal endpoint A leased from the
quarantine server; release, the automatic bounce, and `drop` behaved as
predicted; in Part F the 802.1X session showed the quarantined MAC address. Track
2: the entry and settings were built and the predictions are answered.

**Negative test:** Disable the feature with endpoint A in `qtn-174`, then
enable it again:

```text
FGT # config user quarantine
set quarantine disable
end
```

Predict and observe (with the bounce still enabled): endpoint A returns to
`fsw-users` although its entry still exists, because disabling the feature
releases every quarantined MAC address (p. 272). Set `quarantine enable` (or
your recorded value) and record whether endpoint A goes back to quarantine.
Track 2: prediction 2 is the negative test.

**Rollback:** Delete the entry, restore the global settings to the values
recorded in step 1 (shown here as the defaults), and take the security policy
off `port2`:

```text
FGT # config user quarantine
set quarantine enable
config targets
delete "qtn-174"
end
end
FGT # config switch-controller global
set bounce-quarantined-link disable
end
FGT # config switch-controller managed-switch
edit <SWITCH_SN>
config ports
edit "port2"
unset port-security-policy
next
end
next
end
```

Bounce endpoint A's link and confirm a `fsw-users` lease and a working ping to
`10.174.41.1`; confirm that endpoint B reaches `10.174.43.1` and that `show
switch vlan 4093` lists no `member-by-mac` entry.

**Lab verified by:** *pending*

### Lab 9.4 — IGMP snooping, querier, and multicast flood control

**Objective:** Show unregistered multicast flooding in `fsw-users`, enable IGMP
snooping and see it pruned, join a group and see it forwarded, watch the group
age out without a querier and stay with one, control flooding per switch and
per port, check MCLAG IGMP-snooping awareness on S3, and predict MLD snooping.

**Platform notes:** Hands-on on C1 and C3 (and C2 with a lab-VLAN GO) with S1,
S2, or S3 (on S3, `FSW-A`): IGMP snooping, proxy, and querier are chain in both
columns; S1 and S2 allow snooping on at most 5 VLANs (note 23), and this lab
uses one. On S2 a 239.x.x.x group floods whatever the settings (FortiLink Guide
7.6.7, p. 147), so the lab uses `233.252.0.174` and step 10 tests 239 apart.
Step 3 (MCLAG awareness) is S3 only. MLD snooping is read-and-predict on every
option. Track 2: the VLAN, global, and per-switch settings run live (the
per-switch block on the stand-in entry if it exists); the endpoint and switch
steps are read-and-predict.

**Track 1:**

1. Put endpoint B in `fsw-users` as in Chapter 08 and give it the static
   address there:

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
   ping -c 3 10.174.41.1
   ```

2. Baseline without snooping. On endpoint A capture the group; on endpoint B
   send for 30 seconds:

   ```bash
   # endpoint A
   sudo timeout 40 tcpdump -ni <IFACE> -c 20 host 233.252.0.174
   # endpoint B
   iperf -c 233.252.0.174 -u -T 1 -B 10.174.41.20 -b 100K -t 30
   ```

   Predict. **Answer:** endpoint A captures 20 packets although it never joined:
   without snooping, the switch floods multicast to every port in the VLAN.

3. On S3, check MCLAG IGMP-snooping awareness on both switches before enabling
   snooping:

   ```text
   FSW # get switch global
   FGT # show switch-controller managed-switch <SWITCH_SN>
   ```

   Record `mclag-igmpsnooping-aware` on `FSW-A` and `FSW-B`. Predict.
   **Answer:** the sources disagree: the FortiLink Guide says enabled (p. 85),
   the FortiSwitchOS 7.6.7 CLI Reference `disable` (p. 118), and the FortiOS
   7.6.0 option that pushes it, `mclag-igmp-snooping-aware`, defaults to
   `enable` (a missing line in `show` means the default). If either switch shows
   `disable`, enable it from the controller for that switch (`<SWITCH_SN>` and
   then `<FSWB_SN>`) and read again:

   ```text
   FGT # config switch-controller managed-switch
   edit <SWITCH_SN>
   set mclag-igmp-snooping-aware enable
   next
   end
   ```

   Also record `igmp-snooping-flood-reports` and `mcast-snooping-flood-traffic`
   on the ICL trunk (`show switch interface <ISL_PORT>` trunk name from Lab 6.3)
   and the FortiLink trunk `<FL_TRUNK>`: the guide wants them enabled on the ICL
   and disabled on ISL and FortiLink trunks (p. 85).

4. Read the global settings on both sides:

   ```text
   FGT # get switch-controller igmp-snooping
   FSW # get switch igmp-snooping globals
   ```

   Record `aging-time` (300) and `query-interval`: FortiOS's default is 125,
   the switch reference's 120 (p. 125); record which the switch shows.

5. Enable IGMP snooping on `fsw-users` and read the switch:

   ```text
   FGT # config system interface
   edit "fsw-users"
   set switch-controller-igmp-snooping enable
   next
   end
   FSW # get switch igmp-snooping status
   ```

   `IGMP-SNOOPING enabled vlans` should list 1741. Record `Max multicast
   snooping groups`.

6. Repeat step 2. Predict. **Answer:** endpoint A captures nothing (tcpdump
   times out): `233.252.0.174` is now unregistered multicast, which goes only to
   mRouter ports and ports with `mcast-snooping-flood-traffic`
   (`flood-unknown-multicast` is disabled; Administration Guide, p. 313).

7. Join the group on endpoint A, watching IGMP in a second window, and read
   the group table:

   ```bash
   # endpoint A
   sudo tcpdump -ni <IFACE> igmp
   sudo ip address add 233.252.0.174/32 dev <IFACE> autojoin
   ```

   ```text
   FSW # get switch igmp-snooping group
   FGT # diagnose switch-controller switch-info igmp-snooping group <SWITCH_SN>
   ```

   The capture shows endpoint A's membership reports (IGMPv3 by default on
   Linux). The switch lists group `233.252.0.174` in VLAN 1741 on `port1`; the
   controller command is from the FortiOS 8.0.1 CLI Reference (cross-check).
   Repeat step 2: endpoint A now captures the stream.

8. Make the group age quickly and watch it go without a querier. Override the
   aging time on this switch only (it must stay above the 125 s query
   interval):

   ```text
   FGT # config switch-controller managed-switch
   edit <SWITCH_SN>
   config igmp-snooping
   set local-override enable
   set aging-time 150
   end
   next
   end
   ```

   Wait three minutes without touching endpoint A, then repeat `get switch
   igmp-snooping group` and step 2. Predict. **Answer:** the group is gone and
   endpoint A receives nothing: no device sends IGMP queries in `fsw-users`
   (the FortiGate runs no multicast routing there), so endpoint A sent no report
   after its join, and the entry aged out.

9. Enable the proxy and the querier for `fsw-users`; the guide requires
   snooping and the proxy on the VLAN before the querier (p. 148):

   ```text
   FGT # config system interface
   edit "fsw-users"
   set switch-controller-igmp-snooping-proxy enable
   next
   end
   FGT # config switch-controller managed-switch
   edit <SWITCH_SN>
   config igmp-snooping
   config vlans
   edit "fsw-users"
   set querier enable
   set version 2
   next
   end
   end
   next
   end
   ```

   Re-join on endpoint A (`sudo ip address del 233.252.0.174/32 dev <IFACE>`,
   then step 7's `add`), and watch the IGMP capture for five minutes. Predict.
   **Answer:** membership queries arrive about every query interval, endpoint A
   answers each with a report (version 2 after it hears version 2 queries), and
   the group stays in the table past 150 s. Record the queries' source address
   (no `querier-addr` was set) and interval, and confirm with step 2 that the
   stream still arrives.

10. Flood control. Leave the group on endpoint A (`sudo ip address del
    233.252.0.174/32 dev <IFACE>`), then flood multicast to `port1` only and
    repeat step 2:

    ```text
    FGT # config switch-controller managed-switch
    edit <SWITCH_SN>
    config ports
    edit "port1"
    set mcast-snooping-flood-traffic enable
    next
    end
    next
    end
    ```

    Endpoint A receives the stream without a join: the port floods unregistered
    multicast (Administration Guide, p. 313). Set it back to `disable`, then try
    the per-switch option `set flood-unknown-multicast enable` under `config
    igmp-snooping` (with `local-override` still enabled) and repeat step 2:
    unregistered multicast now floods to every port in the VLAN (p. 148). Set it
    back to `disable`. On S2 only, also send to `239.1.74.1` with no flood option
    and no join (`iperf -c 239.1.74.1 ...`, capture `host 239.1.74.1`): record
    whether it floods, as the FortiLink Guide says it does on the FS-124F
    (p. 147).

**Track 2:** Run the controller blocks of steps 4, 5, and 9 (the `config
system interface` parts and `get switch-controller igmp-snooping`) on your
controller. If the stand-in entry `S248EPTF18000000` exists (Lab 2.2's second or
third outcome), also run step 8's and step 9's `config igmp-snooping` blocks
against it; step 10's port block needs the third outcome. Check with `show
system interface fsw-users` and `show switch-controller managed-switch
S248EPTF18000000`.

**Track 2: read-and-predict.**

1. The FortiSwitchOS 7.6.7 CLI Reference prints this group table (p. 497),
   trimmed:

   ```text
   Number of Groups: 7
   port        of-port VLAN GROUP     Age
   (__port__9)   1     23   231.8.5.4 16
   (__port__43)  3     23   querier   17
   (__port__14)  8     --- flood-reports ---
   (__port__10)  2     --- flood-traffic ---
   ```

   Predict what the last two lines mean. **Answer:** those ports have
   `igmp-snooping-flood-reports` and `mcast-snooping-flood-traffic` enabled, so
   they receive reports and unregistered multicast regardless of joins; the
   `querier` line marks the port toward the querier (an mRouter port).
2. An FS-124F runs IGMP snooping on five VLANs, and an administrator enables it
   on a sixth. Predict. **Answer:** refused or not applied: note 23 allows five
   on the FS-1xxE/F/G series; record the message if you test it.
3. An IPv6 host on an S3 VLAN joins an IPv6 multicast group while IGMP
   snooping is on. Predict whether the managed switch prunes the IPv6 stream.
   **Answer:** no: MLD snooping is a dash in the 200 Series column and FortiOS
   7.6.0 has no MLD option for managed switches. Unregistered IPv6 multicast
   shares the unregistered IPv4 flooding behavior while IGMP snooping is on
   (Administration Guide, p. 313), so it reaches only mRouter and flood-traffic
   ports, which can starve IPv6 listeners; the guide's advice is to run both
   snooping types or neither on such a VLAN.

**Expected result:** Track 1: without snooping the stream flooded to endpoint
A; with snooping it stopped until endpoint A joined; without a querier the
group aged out after the 150 s override, and with the proxy and querier it
stayed, with queries visible on endpoint A; the two flood options each brought
the stream back; on S3 `mclag-igmpsnooping-aware` was read on both switches;
on S2 the 239.x behavior is recorded. Track 2: the settings were built and the
predictions are answered.

**Negative test:** With the querier running and endpoint A joined, leave the
group (`sudo ip address del 233.252.0.174/32 dev <IFACE>`) while endpoint B
sends. Predict and observe: endpoint A sends a leave, the switch's proxy sends
a group-specific query, and the stream stops within about the
`leave-response-timeout` (10 s on the switch, p. 125) or at the latest when the
entry ages out; record which. Track 2: prediction 1 is the negative test.

**Rollback:** Remove the per-switch and port settings first, then the VLAN
settings, then put `port2` and the endpoints back:

```text
FGT # config switch-controller managed-switch
edit <SWITCH_SN>
config igmp-snooping
config vlans
delete "fsw-users"
end
set flood-unknown-multicast disable
unset aging-time
set local-override disable
end
config ports
edit "port1"
set mcast-snooping-flood-traffic disable
next
edit "port2"
set vlan "fsw-iot"
next
end
next
end
FGT # config system interface
edit "fsw-users"
set switch-controller-igmp-snooping-proxy disable
set switch-controller-igmp-snooping disable
next
end
```

If you changed `mclag-igmp-snooping-aware` in step 3, leave it enabled: it is
the FortiOS default and harmless without snooping. Then:

```bash
# endpoint A
sudo ip address del 233.252.0.174/32 dev <IFACE>
# endpoint B
sudo ip addr del 10.174.41.20/24 dev <IFACE_B>
ping -c 3 10.174.43.1
```

Confirm that `get switch igmp-snooping status` lists no snooping VLAN, that
endpoint A reaches `10.174.41.1`, and that `show switch-controller
managed-switch <SWITCH_SN>` shows `port1` and `port2` as Chapter 08 left them.
Restore `fgt-pre-9-1-174.conf` only if something else differs.

**Lab verified by:** *pending*

## Lab Verification

Complete this sign-off once Labs 9.1 to 9.4 have been run end to end, including
each negative test. Until then, the labs are unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The FortiGate learns about devices behind a managed switch from its own device
identification and from the switch's MAC, LLDP, and DHCP-snooping databases,
plus network monitoring on the 200 Series. A NAC policy matches such a device
on a NAC-mode port and its MAC policy moves the device into a VLAN; unmatched
devices wait in the onboarding VLAN, and a dynamic firewall address carries the
match into firewall policy. LAN segments keep a device's address across NAC
VLANs, but only one segment exists, its VLANs have no Layer 3 settings, and the
FS-108F cannot be cabled directly to the FortiGate for it. A dynamic port
policy changes the port instead: VLAN policy, LLDP profile, QoS policy, or
802.1X policy for whatever device matches. Quarantine-by-VLAN binds a MAC
address to the quarantine access VLAN on the switch, which every host port must
carry, and `bounce-quarantined-link` makes DHCP clients follow. IGMP snooping
prunes multicast to joined ports, needs a querier (after the proxy) to keep
groups alive, has flood options per switch and per port, is limited to five
VLANs on the FS-1xx models, and has no MLD counterpart on the lab's switches.
The chapter ends with every setting removed and the C2 slot P3 free.

- [ ] I read endpoint B's entry in the device list and know whether my switch
      supports network device detection.
- [ ] Endpoint B waited in the onboarding VLAN and moved to `fsw-iot` when
      `nac-iot-174` matched, and P3 let only the matched device reach
      `fsw-users`.
- [ ] I can say why NAC LAN segments are read-and-predict here.
- [ ] `dpp-174` gave `port2` its VLAN policy, LLDP profile, and QoS policy, and
      I recorded whether a vendor match worked.
- [ ] Quarantining endpoint A moved it to VLAN 4093 and the quarantine DHCP
      server; release, the automatic bounce, and `drop` behaved as predicted.
- [ ] IGMP snooping pruned an unjoined stream, forwarded a joined one, and kept
      it only with the querier; I tested both flood options.
- [ ] On S3, I recorded `mclag-igmpsnooping-aware` on both switches.
- [ ] Every setting from Labs 9.1 to 9.4 is removed, `port1` and `port2` are as
      Chapter 08 left them, and on C2 P3 is free.
