# Chapter 08: Filtering, Antispoofing, ACLs, and VLAN Security

## Learning Objectives

- Explain how **DHCP snooping** builds a binding database from the DHCP
  exchanges it sees, why the port toward the real DHCP server must be
  **trusted**, and how a rogue DHCP server on an access port is stopped; enable
  it on a FortiSwitch VLAN from the FortiGate, insert **option 82** data, and
  restrict replies to an **allowed DHCP server list**.
- Enable **dynamic ARP inspection (DAI)** on a VLAN that already has DHCP
  snooping, see a spoofed ARP packet dropped, and admit a statically addressed
  host with a **DHCP-snooping static entry**; state where **IP source guard**
  works (the 200 Series, not the FS-108F or FS-124F) and test it where it does.
- Configure **storm control** globally, per switch, and per port through a
  storm-control policy, measure its effect on a broadcast flood, and state the
  FS-1xx limits in feature matrix note 21.
- Build a FortiLink-mode **ACL ingress policy** and **ACL group**, apply it to
  a managed port, and read its counters; explain why only the ingress stage is
  available in FortiLink mode and why the FS-108F and FS-124F have no ACLs in
  FortiLink mode at all (note 16).
- **Block intra-VLAN traffic** on a FortiSwitch VLAN, then let selected hosts
  talk again through the FortiGate with proxy ARP and a firewall policy (the
  C2 budget's free slot, P3); apply native VLAN hygiene to access and unused
  ports; and predict the behavior of a **private VLAN**, which is a standalone
  feature on the 200 Series only.

## Theory and Architecture

### Where each control lives in FortiLink mode

Every control in this chapter is configured on the FortiGate and pushed to the
managed switch, but the objects sit in different places in FortiOS. The table
is the map for the rest of the chapter (FortiOS 7.6.0 CLI Reference; FortiLink
Guide 7.6.7, pp. 144–146 and 247–263):

| Control | Scope | FortiOS object | Key options |
| --- | --- | --- | --- |
| DHCP snooping | Per VLAN | `config system interface` (the FortiSwitch VLAN) | `switch-controller-dhcp-snooping`, `-option82`, `-verify-mac`; `config dhcp-snooping-server-list` |
| DHCP trust | Per port | `config switch-controller managed-switch`, `config ports` | `dhcp-snooping {untrusted \| trusted}`, `dhcp-snoop-option82-trust` |
| Snooping and option 82 globals | Controller-wide | `config switch-controller global` | `dhcp-server-access-list`, `dhcp-option82-format`, `dhcp-option82-circuit-id`, `dhcp-option82-remote-id`, `dhcp-snoop-client-req`, `dhcp-snoop-client-db-exp`, `dhcp-snoop-db-per-port-learn-limit` |
| Allowed server list switch | Per switch | managed-switch entry | `dhcp-server-access-list {global \| enable \| disable}` |
| DAI | Per VLAN, trust per port | `config system interface`; `config ports` | `switch-controller-arp-inspection {enable \| disable \| monitor}`; `arp-inspection-trust`, `allow-arp-monitor` |
| DHCP-snooping static entries | Per switch | managed-switch entry, `config dhcp-snooping-static-client` | `vlan`, `ip`, `mac`, `port` |
| IP source guard | Per port; bindings per port | `config ports`; managed-switch entry, `config ip-source-guard` | `ip-source-guard enable`; `config binding-entry` (`ip`, `mac`) |
| Storm control | Global, per switch, per port | `config switch-controller storm-control`; managed-switch `config storm-control`; `config switch-controller storm-control-policy` | `rate`, `broadcast`, `unknown-unicast`, `unknown-multicast`; `local-override`; `storm-control-mode` |
| ACLs | Policies and groups global; group per port | `config switch-controller acl ingress`, `config switch-controller acl group`; `config ports` | `config classifier`, `config action`; `ingress`; `acl-group` |
| Intra-VLAN blocking | Per VLAN | `config system interface` | `switch-controller-access-vlan`; `config switch-controller fortilink-settings` `access-vlan-mode` |

### DHCP snooping

**DHCP snooping** watches DHCP on a VLAN and treats each switch port as
**trusted** or **untrusted**. Server messages (OFFER, ACK, NAK) are accepted
only from trusted ports, so a DHCP server plugged into an access port cannot
hand out addresses. From the client exchanges it sees, the switch builds a
**binding database** of MAC address, VLAN, IP address, lease, and port, which
DAI and IP source guard then use. Every port is untrusted by default, and when
a server is detected on an untrusted port the switch logs "A rogue DHCP server
has been detected on the interface"; only the first such server packet per
untrusted interface is logged (FortiSwitchOS 7.6.7 Administration Guide,
p. 276).

In FortiLink mode snooping is enabled **per VLAN** on the FortiGate's VLAN
interface (`set switch-controller-dhcp-snooping enable`) and trust is set **per
port** in the managed-switch entry (`set dhcp-snooping trusted`, default
`untrusted`; FortiLink Guide 7.6.7, pp. 247–249). In this lab the real server
is the FortiGate itself (the `fsw-users` DHCP server on `10.174.41.1`), whose
replies reach the switch over the **FortiLink trunk**, not over a front port. So
the trust state of that trunk decides whether snooping works at all. The
documentation does not state it for the FortiLink trunk; its examples of
switch-formed inter-switch trunks show `set dhcp-snooping trusted` in the
switch configuration (for example the MCLAG ICL on p. 359). Lab 8.1 reads the
FortiLink trunk on the switch and records what your build does.

Three global settings shape the behavior (FortiOS 7.6.0 CLI Reference, `config
switch-controller global`):

| Option | Default | Meaning |
| --- | --- | --- |
| `dhcp-snoop-client-req` | `drop-untrusted` | Client broadcasts (DISCOVER, REQUEST) are sent only to **trusted** ports in the VLAN; `forward-untrusted` sends them to all ports |
| `dhcp-snoop-client-db-exp` | 86400 | Seconds an entry stays in the snooping server database (300–259200) |
| `dhcp-snoop-db-per-port-learn-limit` | 64 | Binding entries per port; the reference text says 0–1024 but prints a maximum of 2048, and the guide says the range depends on the model, so check it with `?` (p. 250) |

`dhcp-snoop-client-req` matters for the rogue-server test. With the default, a
client's DISCOVER never reaches a host on another untrusted port, so a rogue
server there does not even see the request; with `forward-untrusted` it sees
the request and answers, and the switch drops the answer at the rogue's port.
Lab 8.1 shows both.

Model limits: note 15 of the feature matrix allows DHCP snooping on at most 25
VLANs on the FS-1xxE, FS-1xxF, and FS-1xxG models (S1 and S2), and 4,096 on
the 200 Series. Ports shared between VDOMs do not support DHCP snooping
(FortiLink Guide 7.6.7, p. 125), which matters in Chapter 10.

### Option 82 and the allowed DHCP server list

**Option 82** (the DHCP relay agent information option) lets the switch insert
a **circuit ID** and a **remote ID** into the client's DHCP requests, so that
the server knows which switch port a request came from (FortiOS 7.4.0 and
FortiSwitchOS 7.2.2 or later; FortiLink Guide 7.6.7, pp. 249–251). It is
enabled per VLAN with `switch-controller-dhcp-snooping-option82 enable`. The
format is global: `dhcp-option82-format ascii` (the default) builds the fields
from `dhcp-option82-circuit-id` (default `intfname vlan mode`) and
`dhcp-option82-remote-id` (default `mac`); `legacy` uses a fixed binary layout.
A per-port, per-VLAN override (`config dhcp-snoop-option82-override` under the
port, with `circuit-id` and `remote-id`) replaces both fields with plain text.
The guide prints the override's option as `remode-id` (p. 251); the FortiOS
7.6.0 reference names it `remote-id`. On an untrusted port, a DHCP packet that
already carries option 82 is dropped unless `dhcp-snoop-option82-trust enable`
is set on that port.

The **allowed DHCP server list** goes one step beyond trust: when it is on,
only servers in the list may answer, even on trusted ports (FortiOS 7.0.1 and
later; pp. 247–249). It takes three settings: `dhcp-server-access-list enable`
under `config switch-controller global`, `dhcp-server-access-list global` (the
default) or `enable` in the managed-switch entry, and a
`config dhcp-snooping-server-list` entry with `server-ip` on the VLAN interface.
Each table holds up to 255 servers, with 2,048 across all VLANs. On the switch,
`get switch dhcp-snooping server-db-details` then shows `allowed` or `blocked`
in its `svr-list` column (FortiSwitchOS 7.6.7 CLI Reference, p. 494).

### Dynamic ARP inspection and static entries

**DAI** checks each ARP packet that arrives on an untrusted port against the
DHCP-snooping binding database and drops packets whose sender IP and MAC
address do not match a binding (FortiLink Guide 7.6.7, pp. 251–252). That stops
the classic man-in-the-middle trick of announcing another host's IP address
with your own MAC address. Three settings are needed, in order: DHCP snooping on
the VLAN, `switch-controller-arp-inspection enable` on the VLAN interface, and
`arp-inspection-trust` on the ports (default `untrusted`; FortiOS 7.6.0 CLI
Reference). The guide's syntax lines contain two typos, `set
switch-controller-arp-inpsection` and an `arp-inspection-trust` line without
`set` (p. 252); use the 7.6.0 spellings. The switch-side reference says
`arp-inspection` cannot be set to `enable` or `monitor` unless `dhcp-snooping`
is enabled on the VLAN (FortiSwitchOS 7.6.7 CLI Reference, p. 186).

The same trust question applies as for snooping: the FortiGate's own ARP
replies arrive over the FortiLink trunk, and its address is in no binding. If
that trunk were untrusted for ARP, enabling DAI would cut every host off from
its gateway. The documentation does not say; Lab 8.2 records it.

A host with a static address has no binding, so DAI drops its ARP. A
**DHCP-snooping static entry** binds one IPv4 address to one MAC address on one
port and VLAN (FortiLink Guide 7.6.7, pp. 253–254). Its rules: the port must not
be trusted and must not be an 802.1X port; one MAC address per entry; at most 64
entries per switch; once an entry exists, its VLAN cannot be removed from the
port and the port cannot join a trunk until the entry is deleted. The guide
prints `set vlan` with a VLAN ID (`100`); the FortiOS 7.6.0 reference describes
the field as a VLAN **name** of up to 15 characters, and this chapter uses the
name.

**ARP monitoring** (`switch-controller-arp-inspection monitor` on the VLAN and
`allow-arp-monitor enable` on a trusted port, FortiOS 7.4.4 and later) records
IP and MAC pairs from ARP packets into the snooping database instead of
dropping anything (p. 252). On the switch, such entries carry an `A` flag in the
client database, static entries an `S` flag, and entries learned in snooping
monitor mode a `D` flag (Administration Guide, p. 283).

### IP source guard

**IP source guard** filters IPv4 **data** traffic on a port: only source
addresses from a binding are forwarded, either a dynamic binding learned by
DHCP snooping or a static `binding-entry` (FortiLink Guide 7.6.7, pp. 254–256).
It is off by default and is enabled per port with `set ip-source-guard enable`.
Discarded packets are not logged. Static entries win over dynamic ones, and
more than 2,048 entries from a FortiGate produce an error. On the switch,
disabling IP source guard on a port removes all of that port's static and
dynamic entries, and the feature does not work with VLAN translation
(Administration Guide, p. 285).

The guide says IP source guard can be configured in FortiOS only for managed
switches that support it (p. 254). The feature matrix marks it as not supported
in the 1xxE/1xxF column and supported in both modes on the 200 Series, so it is
hands-on only on S3. The **IP source-guard violation log** (`config
switch-controller ip-source-guard-log`) is from **FortiOS 7.6.4**; it is not in
the 7.6.0 reference, so on FGT-1 (7.6.2) it is read-only here, and the switch
side reads it with `get switch ip-source-guard-violations all` (p. 256).

### Storm control

**Storm control** measures broadcast, unknown unicast, and unknown multicast
traffic in packets per second and drops what exceeds the rate (FortiLink Guide
7.6.7, pp. 144–146). Each type is enabled separately and all three are disabled
by default; the rate is 1 to 10,000,000 packets per second, default 500, and 0
drops all traffic of the enabled types. FortiOS offers three levels:

| Level | FortiOS object | Applies to |
| --- | --- | --- |
| Global | `config switch-controller storm-control` | All ports of all managed switches, **FortiLink ports included** (p. 145) |
| Per switch | `config storm-control` under the managed-switch entry, with `local-override enable` | All ports of one switch |
| Per port | `config switch-controller storm-control-policy`, applied with `storm-control-policy` under `config ports` | One port |

A storm-control policy has `storm-control-mode`: `global` (the default; use the
global or switch-level settings), `override` (use the policy's own rate and
types), or `disabled` (no storm control on the port at all, whatever the global
and switch settings say). The FortiOS 7.6.0 reference gives `default` as the
default value of a port's `storm-control-policy`, which is a policy name;
Lab 8.3 records whether a policy of that name exists on your controller.

On the switch, the same settings appear in `config switch storm-control`
(global) and in `config switch physical-port` with `storm-control-mode
override` and a `config storm-control` block (per port), and the switch accepts
a rate of 0 or 2 to 10,000,000 (FortiSwitchOS 7.6.7 CLI Reference, p. 176;
Administration Guide, pp. 359–361). Two related features are newer or
narrower:

- **Burst size** (`burst-size-level`, 0 to 4) is in FortiOS from **7.6.4**
  (p. 145) and in FortiSwitchOS from 6.4.3; FGT-1 runs 7.6.2, so this chapter
  only reads about it. The FS-124E models cannot set it per port.
- **Storm-control monitoring** (`storm-control-monitor`,
  `storm-control-high-rate`, `storm-control-rate-filter` under `config switch
  global`, FortiSwitchOS 7.4.3 and later) is a standalone feature (check mark in
  the matrix), and note 21 says the FS-1xxE and FS-1xxF models do not support
  `storm-control-high-rate` or `storm-control-rate-filter` at all.

Storm control does not stop a loop; Chapter 05 used it only as a backstop.

### ACLs in FortiLink mode

A FortiSwitch has three ACL stages in standalone mode: **prelookup** (before
the forwarding lookup), **ingress**, and **egress**. In FortiLink mode only the
**ingress** stage is available (feature matrix note 16), from FortiOS 7.4.0 with
FortiSwitchOS 7.4.0 (FortiLink Guide 7.6.7, pp. 256–260). An ingress policy
acts on traffic arriving on the port it is applied to, never on traffic leaving
it.

| Piece | FortiOS object | Content |
| --- | --- | --- |
| ACL ingress policy | `config switch-controller acl ingress`, `edit <id>` | `config classifier` (source and destination MAC, VLAN, source and destination IPv4 prefix), `config action` (`drop`, `count`), `description` |
| ACL group | `config switch-controller acl group`, `edit <name>` | `set ingress <id> ...`; the order of the classifiers matters for hardware allocation |
| Port binding | `config ports`, `set acl-group "<group> ..."` | One or more groups per port |
| Counters | `diagnose switch-controller switch-info acl-counters <SWITCH_SN>` | Packet counts per policy; byte counters always read 0 on the FS-4xxE, FS-1xxE, and FS-1xxF (p. 259) |

The switch matches ACLs in **TCAM**, a fixed hardware table, and allocates it
best-fit in classifier order, so an ACL can fail to install when the table is
fragmented; on the switch, `get switch acl usage` shows the free entries
(FortiSwitchOS 7.6.7 CLI Reference, p. 493). The controller's ingress policies
go into **ACL group 3** on the switch, and a switch without group 3 cannot use
them (FortiLink Guide 7.6.7, p. 258). A user ACL can also conflict with ACLs
that other managed-switch features install internally, and the guide advises
testing every user ACL with the features you run (p. 257).

Model support is blunt. Note 16 lists the FS-108F and FS-124F (with their POE
and FPOE variants) among the models that do **not support ACL in FortiLink
mode**, together with other FS-1xx, FS-3xxG, FS-6xxF, and FortiSwitch Rugged
models; the 1xxE/1xxF column marks IPv4 ingress ACLs as standalone-only. The 200 Series supports ingress ACLs in both modes. The
prelookup and egress stages are not supported in the 1xxE/1xxF column **or** in
the 200 Series column, so no option in this volume uses them; multiple ingress
ACLs per port, ACL schedules, and ACL services are standalone features. So
Lab 8.4 is hands-on on S3; on S1 and S2 the ACL exercise moves to Lab 11.4,
where the same switch runs standalone.

Dynamic ACLs from RADIUS (DACLs, Chapter 07) are a separate feature: the matrix
marks them supported in both modes in the 1xxE/1xxF and 200 Series columns.

### Blocking intra-VLAN traffic

With `switch-controller-access-vlan enable` on a FortiSwitch VLAN interface,
the managed switches block port-to-port traffic in that VLAN; hosts can reach
only the FortiGate (FortiLink Guide 7.6.7, pp. 261–263). Chapters 03 and 04 met
the result as an **access VLAN**: the auto-created quarantine VLAN is one, and
note 7 limits the FS-108F and FS-124F to 16 of them. The FortiGate can then
decide which host-to-host traffic to allow, which takes three things:

1. **Proxy ARP** on the FortiGate (`config system proxy-arp`), because a
   host's ARP request for its neighbor no longer reaches the neighbor; the
   FortiGate answers with its own MAC address instead. FortiOS 7.4.2 and later
   allow 256 entries of up to 1,024 addresses each.
2. **`allow-traffic-redirect disable`** under `config system global`. The guide
   requires it when traffic enters and leaves the FortiGate on the same
   interface (p. 261); the 7.6.0 reference describes the enabled default as
   forwarding such traffic **without a policy check**.
3. A **firewall policy** for the traffic. `fsw-users` is a member of the
   `FSW-LAN` zone, and FortiOS configures policies for a zone instead of for
   the individual interfaces in it (7.6.0 reference, `config system zone`), so
   the policy runs from `FSW-LAN` to `FSW-LAN`. The zone's `intrazone deny`
   governs traffic between **different** member interfaces; traffic that leaves
   on the interface it arrived on needs the policy in any case.

The guide adds that IPv6 between clients is not supported when intra-VLAN
blocking is on, and that blocking does not work when the FortiLink interface is
a hardware or software switch. What the switches do when they lose the
FortiGate is set per FortiLink interface by `access-vlan-mode` under `config
switch-controller fortilink-settings` (FortiOS 7.4.1 with FortiSwitchOS 7.4.1):
`legacy` (the default, behavior as in 7.4.1 and earlier), `fail-open` (allow
intra-VLAN traffic), or `fail-close` (keep blocking it). On the switch side,
FortiSwitchOS 7.6.5 and later can enable DHCP snooping, ARP inspection, and
access-VLAN on the same switch VLAN (Administration Guide, p. 276); on an
earlier build, do not combine them, which is why Lab 8.5 runs after Labs 8.1
and 8.2 have turned snooping off.

### Private VLANs and other standalone-only controls

A **private VLAN** divides a primary VLAN into secondary VLANs that keep the
primary's subnet (Administration Guide, pp. 355–356). Ports in the one
**isolated** VLAN reach only **promiscuous** ports (the gateway side); ports in
a **community** VLAN reach each other and the promiscuous ports; neither
reaches another secondary VLAN. It is configured on the switch (`config switch
vlan` with `private-vlan enable`, `isolated-vlan`, and `community-vlans`;
`config switch interface` with `private-vlan promiscuous` or `sub-vlan`). The
matrix marks private VLANs as not supported in the 1xxE/1xxF column and as
standalone-only on the 200 Series, so in FortiLink mode intra-VLAN blocking is
the tool, and private VLANs are read-and-predict here. **IPv6 RA guard** and
**DHCPv6 snooping** are in the same position: not supported on the FS-1xx
column, standalone-only on the 200 Series.

### Model support for this chapter

From the FortiSwitchOS 7.6.7 feature matrix (`temp/nse5fsw/fm767.txt`, the
position-based read); chain = standalone and managed, check = standalone only,
dash = not supported:

| Feature | 1xxE/1xxF (S1 FS-108F, S2 FS-124F) | 200 Series (S3) | Note |
| --- | --- | --- | --- |
| DHCP snooping | Chain | Chain | Note 15: 25 VLANs on FS-1xxE/1xxF/1xxG; 4,096 on the 200 Series |
| DHCP-snooping static entries, option 82, allowed DHCP server list | Chain | Chain | |
| DHCP-snooping monitor mode | Check | Check | Standalone only |
| DHCPv6 snooping | Dash | Check | |
| Dynamic ARP inspection, DAI ARP monitoring | Chain | Chain | |
| IP source guard, IP source-guard violation log | Dash | Chain | Violation log needs FortiOS 7.6.4 in FortiLink mode |
| Storm control, per-port storm control, global burst-size control | Chain | Chain | Burst size needs FortiOS 7.6.4 |
| Storm-control monitoring | Check | Check | Note 21: no `storm-control-high-rate` or `storm-control-rate-filter` on FS-1xxE/1xxF |
| ACL (IPv4 ingress) | Check | Chain | Note 16: no ACL in FortiLink mode on the FS-108F and FS-124F (all variants) |
| ACL (IPv4 egress), ACL (IPv4 prelookup) | Dash | Dash | |
| Multiple ingress ACLs | Dash | Check | |
| ACL service, schedule for ACLs | Check | Check | |
| Dynamic ACLs (IPv4) | Chain | Chain | |
| Block intra-VLAN traffic | Chain | Chain | Note 7: 16 access VLANs on FS-1xxE, FS-108F, FS-124F |
| Private VLANs | Dash | Check | |
| IPv6 RA guard | Dash | Check | |

## Design Considerations

### Exam tasks this chapter practices

| Exam task | Labs here | Track 2 mode |
| --- | --- | --- |
| 3.2 Filtering and antispoofing | 8.1, 8.2, 8.3 (primary) | Build + predict |
| 3.3 ACLs, security profiles, VLAN security | 8.4, 8.5 (primary) | Build + predict |
| 4.1 Packet capture | 8.1 negative test (FortiGate sniffer on the VLAN) | Predict; the live sniffer is Track 1 only |
| 4.3 View and extract information | 8.2 (binding database, DAI statistics) | Predict |
| 1.1 VLANs | 8.5 (VLAN hygiene) | Build + predict |

### One test VLAN, and endpoint B as a second host in it

Every test in this chapter needs two hosts in one VLAN with a DHCP server, and
`fsw-users` (1741) is the only lab VLAN with one. So each lab moves `port2`
(endpoint B) into `fsw-users` for its duration and gives endpoint B a second,
static address `10.174.41.20/24` next to its `10.174.43.20`, outside the
FortiGate's DHCP pool (`.100`–`.199`). The lab's rollback moves `port2` back to
`fsw-iot` and removes the address. `set vlan` changes only the native VLAN; no
lab here touches `allowed-vlans`, so `quarantine` stays allowed on both ports.

| Role | Host | Port | Address in `fsw-users` |
| --- | --- | --- | --- |
| Legitimate client | Endpoint A | `port1` | DHCP lease from `10.174.41.1`, recorded as `<LEASE_A>` |
| Rogue DHCP server, static host, second host | Endpoint B | `port2` (temporarily native `fsw-users`) | `10.174.41.20/24` (static) |
| Rogue server's pool | `dnsmasq` on endpoint B | — | `10.174.41.210`–`.220`, gateway `10.174.41.20` |
| Spoofed addresses | Endpoint A | `port1` | `10.174.41.50`, `.51`, `.52` (never leased) |

`port1` and `port2` keep BPDU guard (Chapter 05); nothing in this chapter plugs
a bridge into them.

### The C2 budget and the C2 lab-VLAN NO-GO

No lab adds an interface or a route. Lab 8.5 Part A uses **P3**, the C2
evaluation's one free policy slot, for the intra-VLAN policy and deletes it in
its rollback; an address object and a proxy ARP entry do not count against the
caps. If Lab 4.1 sent you down its branch that uses P3 for an internet policy
with NAT, Lab 8.5 step 7 is read-and-predict on C2. On C1 and C3 there is no
cap.

After a C2 lab-VLAN NO-GO in Lab 4.1, `fsw-users` does not exist on C2. Labs
8.1 and 8.2 and Lab 8.5 Part A need it and its DHCP server, so run them on C1 or
C3 or read-and-predict them. Labs 8.3 and 8.4 run on C2 with the auto-created
`video` VLAN (4090) in place of `fsw-users`, both endpoints on static addresses
in a subnet of your choice, and `4090` in Lab 8.4's classifier.

### Lab order and state

| Lab | Builds | Rollback leaves |
| --- | --- | --- |
| 8.1 | Snooping, option 82, and the server list on `fsw-users`; `port2` in `fsw-users` | All of it removed; global snooping settings at defaults |
| 8.2 | Snooping again, then DAI, a static entry for endpoint B, and IP source guard on `port1` (S3) | All of it removed |
| 8.3 | `storm-174` on `port1` | Policy removed and deleted |
| 8.4 | `acl-174` (ACL 1) on `port1` (S3) | Group unbound and deleted, ACL deleted |
| 8.5 | Access VLAN on `fsw-users`, proxy ARP, P3, `discard-mode` on `port1`, `port4` shut | All of it removed; `allow-traffic-redirect` restored |

Each lab is self-contained: its rollback returns `FSW-A`'s ports and the
global settings to the state Chapter 07 left, and the next lab rebuilds what it
needs. On S3, the VLAN-level settings (snooping, DAI, access VLAN) reach `FSW-B`
too, because they belong to the VLAN; only `FSW-A`'s ports are used.

### What to keep after this chapter

Nothing. The chapter ends with `fsw-users` as Chapter 04 built it, no
storm-control policy or ACL objects, `port1` and `port2` as Chapter 07 left
them, `port4` up with no description, `allow-traffic-redirect` at its recorded
value, and P3 free on C2. The 802.1X objects of Chapter 07 are untouched.

## Implementation and Automation

The labs are the implementation. Four habits make them traceable.

**Watch DHCP on the wire.** On endpoint A, `tcpdump` with `-e` prints the
source MAC and IP address of every OFFER, which tells you which server
answered. Run it in a second window during Lab 8.1:

```bash
# endpoint A
sudo tcpdump -ni <IFACE> -e 'udp port 67 or udp port 68'
```

**Read both sides.** The controller shows what it pushed; the switch shows what
it enforces. Keep a console or SSH session to the switch open and compare, for
example, the controller's and the switch's view of the binding database:

```text
FGT # diagnose switch-controller switch-info dhcp-snooping database <SWITCH_SN>
FSW # get switch dhcp-snooping client-db-details
```

**Get a new lease the same way each time.** Bounce endpoint A's link, as in
Chapter 07; its DHCP client asks again when the link returns:

```bash
# endpoint A
sudo ip link set <IFACE> down && sudo ip link set <IFACE> up
sleep 10; ip -br addr show <IFACE>
```

**Count packets with tcpdump's own summary.** For the storm-control test,
`tcpdump -w /dev/null` stopped with SIGINT prints how many packets it captured,
which avoids counting printed lines.

The FortiOS configuration commands in this chapter were checked against the
FortiOS 7.6.0 CLI Reference. `execute`, `diagnose`, and `get` commands were
checked against the FortiLink Guide 7.6.7 where it prints them
(`switch-info arp-inspection stats`, `switch-info option82-mapping`,
`switch-info ip-source-guard hardware`, `switch-info acl-counters`) and
otherwise against the FortiOS 8.0.1 CLI Reference as a cross-check
(`switch-info dhcp-snooping database`, `diagnose sniffer packet`, `execute dhcp
lease-list`, `diagnose ip arp list`); each is marked where it is used. The
value list of `set ingress` under `config switch-controller acl group` was
matched by hand to the guide's syntax and example (`set ingress 2 3 4`,
p. 258). Switch commands were checked against the FortiSwitchOS 7.6.7 CLI
Reference, with these matched by hand: `diagnose switch physical-ports summary`
takes an optional port argument; `diagnose switch arp-inspection stats` is
printed as a command only in the Administration Guide (p. 288), while the CLI
Reference prints its `clear` form; and `show switch interface`, `show switch
physical-port`, and `show switch vlan` are the `show` forms of the documented
`config` tables (the guides print `show switch interface <trunk>` on p. 359 of
the FortiLink Guide and `show switch physical-port port10` on p. 275 of the
Administration Guide). The endpoint commands follow `dnsmasq(8)`, `tcpdump(8)`,
`arping(8)` (iputils), `ping(8)`, and `ip(8)`.

## Validation and Troubleshooting

| Symptom | Likely cause | Check |
| --- | --- | --- |
| After snooping is enabled, endpoint A gets no lease at all | The FortiGate's replies arrive on an untrusted FortiLink trunk, or the allowed server list is on without `10.174.41.1` in it | `show switch interface <FL_TRUNK>` and `get switch dhcp-snooping server-db-details` on the switch; `show system interface fsw-users` |
| The rogue server still gives out leases | Snooping is not on for the VLAN the endpoints are in, or `port2` is trusted | `get switch dhcp-snooping database-summary` on the switch; `show switch-controller managed-switch <SWITCH_SN>` |
| `dnsmasq` logs no DHCPDISCOVER with snooping on | Expected with `dhcp-snoop-client-req drop-untrusted`: client broadcasts go only to trusted ports | `get switch-controller global` |
| Endpoint A loses its lease after option 82 is enabled | The DHCP server does not accept the inserted option 82 (the documentation does not say how the FortiGate's server treats it) | Disable `switch-controller-dhcp-snooping-option82` and record the result |
| Every host loses its gateway after DAI is enabled | The FortiGate's ARP packets arrive on an ARP-untrusted FortiLink trunk | `show switch interface <FL_TRUNK>`; `diagnose switch-controller switch-info arp-inspection stats <SWITCH_SN>` |
| A static host stops working after DAI is enabled | It has no binding | Add a DHCP-snooping static entry; `get switch dhcp-snooping static-clients` |
| FortiOS refuses a static entry or `port2` cannot leave the VLAN | Static-entry rules: no trusted or 802.1X port; the VLAN cannot be removed while the entry exists | Delete the entry first |
| `set ip-source-guard enable` is refused or has no effect | S1 or S2: not supported (matrix dash) | Your model against the matrix |
| Storm control has no visible effect | The test traffic is below the rate, the policy mode is `global` with global storm control off, or the policy is on the wrong port (it acts where the flood enters) | `show switch physical-port port1` on the switch |
| An ACL does nothing | S1 or S2 (note 16), the group is on the port where the traffic leaves rather than enters, or the classifier's VLAN or prefix does not match | `get switch acl ingress` and `get switch acl counters ingress` on the switch |
| Hosts in an access VLAN still reach each other | `allow-traffic-redirect` is still enabled with proxy ARP in place, or a policy allows it | `get system global`; `show system proxy-arp`; the policy list |
| Hosts in an access VLAN cannot reach each other although a policy exists | No proxy ARP entry covers one of their addresses (each host needs one, so that the other's ARP is answered) | `ip neigh show` on both endpoints; `show system proxy-arp` |

## Security and Best Practices

- **Snoop every user VLAN, trust only the uplinks.** DHCP snooping is the
  foundation for DAI and IP source guard, and the server-access list closes the
  gap a misconfigured trusted port leaves open.
- **Enable DAI after the bindings exist.** Turn snooping on first, let clients
  renew, add static entries for every statically addressed host, and only then
  enable DAI; on a FortiSwitchOS 7.4.3 or later VLAN, ARP monitoring builds the
  table without dropping anything.
- **Use IP source guard where the hardware has it.** On FS-1xx access switches
  DAI is the strongest antispoofing control available in FortiLink mode.
- **Set storm control on host ports, with care on uplinks.** Global storm
  control also applies to FortiLink ports; prefer per-port policies on access
  ports, and never set a rate of 0 for broadcast on a port that needs ARP or
  DHCP.
- **Test every ACL.** User ACLs share TCAM with the switch's own features and
  are allocated in classifier order; check `get switch acl usage` and the
  counters after each change.
- **Isolate hosts that should not talk.** Intra-VLAN blocking moves
  host-to-host traffic through the FortiGate's policy and inspection; keep the
  proxy ARP entries and the policy as narrow as the need.
- **Keep the default VLAN off host and unused ports.** Give host ports a user
  VLAN, discard tagged frames on access ports, and shut unused ports, as the
  Volume CLXXII crosswalks require (Lab 8.5 Part D).

## References and Knowledge Checks

**References**

- [Fortinet, *FortiLink Guide (FortiOS 7.6.7)*](https://docs.fortinet.com/document/fortiswitch/7.6.7/fortilink-guide)
  — shared ports and DHCP snooping (p. 125), DHCP blocking on ports (p. 132),
  storm control (pp. 144–146), DHCP trust and the DHCP server access list
  (pp. 247–249), option 82 (pp. 249–251), DAI and ARP monitoring (pp. 251–252),
  DHCP-snooping static entries (pp. 253–254), IPv4 source guard and its
  violation log (pp. 254–256), ACLs (pp. 256–260), blocking intra-VLAN traffic
  and `access-vlan-mode` (pp. 261–263), switch-formed trunks with
  `dhcp-snooping trusted` (p. 359).
- [Fortinet, *FortiSwitchOS 7.6.7 Administration Guide (Standalone Mode)*](https://docs.fortinet.com/document/fortiswitch/7.6.7/administration-guide)
  — DHCP snooping, the rogue server log, and 7.6.5 VLAN feature combinations
  (pp. 276–284), IP source guard (pp. 285–287), DAI and its statistics
  (pp. 287–289), private VLANs (pp. 355–356), storm control and its monitoring
  (pp. 359–361).
- [Fortinet, *FortiSwitchOS 7.6.7 CLI Reference*](https://docs.fortinet.com/document/fortiswitch/7.6.7/fortiswitchos-cli-reference)
  — `config switch storm-control` (p. 176), `config switch vlan` (`arp-inspection`,
  p. 186), `diagnose switch ip-source-guard hardware entry list` (p. 354),
  `diagnose switch storm-control` (pp. 378–379), `get switch acl` (pp. 492–493),
  `get switch dhcp-snooping` (pp. 493–495), `get switch ip-source-guard`
  (pp. 498–499), `get switch storm-control` (p. 510).
- [Fortinet, FortiOS 7.6 documentation](https://docs.fortinet.com/product/fortigate/7.6)
  — the FortiOS 7.6.0 CLI Reference: `config system interface`
  (`switch-controller-dhcp-snooping`, `-option82`, `-verify-mac`,
  `switch-controller-arp-inspection`, `switch-controller-access-vlan`,
  `dhcp-snooping-server-list`), `config switch-controller global`, `config
  switch-controller managed-switch` (`ports`, `dhcp-snooping-static-client`,
  `ip-source-guard`, `storm-control`), `config switch-controller
  storm-control`, `config switch-controller storm-control-policy`, `config
  switch-controller acl ingress`, `config switch-controller acl group`,
  `config switch-controller fortilink-settings`, `config system global`
  (`allow-traffic-redirect`), `config system proxy-arp`, `config system zone`.
- FortiOS 8.0.1 CLI Reference (cross-check only) — `diagnose
  switch-controller switch-info dhcp-snooping database`, `diagnose sniffer
  packet`, `execute dhcp lease-list`, `diagnose ip arp list`, and the
  `acl-counters <switch> <port>` form.
- FortiSwitchOS 7.6.7 feature matrix (`temp/fsw/FSW-7.6.7-Feature-Matrix.pdf`)
  — the security, ACL, storm control, and private VLAN rows; notes 7, 15, 16,
  and 21.
- [Volume CLXXII, Chapter 11](../../volume-172-disa-srgs-and-stigs/chapters/11-fortiswitch-feature-version-and-srg-map.md),
  [Chapter 33](../../volume-172-disa-srgs-and-stigs/chapters/33-fortiswitch-and-cisco-catalyst-switch-stig-crosswalk.md),
  and
  [Chapter 37](../../volume-172-disa-srgs-and-stigs/chapters/37-cisco-nx-os-switch-and-fortiswitch-stig-crosswalk.md)
  — the SRG requirements and STIG rules behind Lab 8.5 Part D, and the
  prerequisites P12 (DHCP snooping before DAI), P13 (VLANs), and P14 (IP source
  guard bindings).
- [`dnsmasq(8)`](https://manpages.ubuntu.com/manpages/noble/man8/dnsmasq.8.html)
  (`--no-daemon`, `--port=0`, `--dhcp-range`, `--dhcp-option`, `--log-dhcp`),
  [`tcpdump(8)`](https://manpages.ubuntu.com/manpages/noble/man8/tcpdump.8.html),
  [`arping(8)`](https://manpages.ubuntu.com/manpages/noble/man8/arping.8.html)
  (iputils), [`ping(8)`](https://manpages.ubuntu.com/manpages/noble/man8/ping.8.html)
  (`-b`, `-I`, `-i`).

**Knowledge checks**

1. In FortiLink mode, where do you enable DHCP snooping, and where do you set a
   port's trust state?
2. With snooping on and `dhcp-snoop-client-req` at its default, why does a
   rogue server on an access port never see a client's DISCOVER?
3. What must exist before DAI can be enabled on a VLAN, and what happens to a
   host with a static address when DAI is turned on?
4. Which switch options in this volume can run IP source guard, and what are
   its two sources of bindings?
5. Name the three levels of storm control on a FortiGate and the effect of a
   storm-control policy whose mode is `disabled`.
6. Which ACL stage is available in FortiLink mode, on which models, and which
   FortiGate objects does it take?
7. With `switch-controller-access-vlan enable`, what three things does the
   FortiGate need before two hosts in the VLAN can talk again?
8. Why are private VLANs read-and-predict in this chapter on every switch
   option?

## Hands-On Lab

**Shared prerequisites.** Chapter 07 complete: `<SWITCH_SN>` `Authorized/Up`
at `10.255.1.2` with profile `fsw-174-prof` (on S3, `FSW-A`; `FSW-B` is managed
but not used here); `port1` native `fsw-users` (endpoint A, DHCP) and `port2`
native `fsw-iot` (endpoint B, `10.174.43.20/24`), both with BPDU guard and with
no security policy, learning limit, or sticky MAC; `fsw-users` with its DHCP
server (`.100`–`.199`); policies P1 and P2 as Chapter 04 left them, and on C2
P3 free. Endpoint B has `dnsmasq` installed and disabled (Chapter 02). Endpoint
A needs `tcpdump` and `arping`; on Ubuntu or Raspberry Pi OS install them with
`sudo apt install -y tcpdump iputils-arping`, and install `tcpdump` on endpoint
B too. Track 2: the Lab 2.2 pre-provisioning outcome and the stand-in entry
`S248EPTF18000000` if that outcome allowed it. **Cost:** none.

As in earlier chapters, `FGT #` is the controller on any option; the commands
here name VLAN interfaces, not the FortiLink port, so they are the same on C1,
C2, and C3. `<SWITCH_SN>` is your switch's serial number (on Track 2,
`S248EPTF18000000`). `<IFACE>` and `<IFACE_B>` are endpoint A's and endpoint
B's wired interfaces, `<MAC_A>` and `<MAC_B>` their MAC addresses as `ip -br
link` prints them (Lab 2.5 recorded both), and `<LEASE_A>` the address endpoint
A leases in Lab 8.1. `<FL_TRUNK>` is the name of the switch's FortiLink trunk
as Lab 5.1 recorded it (the guide's example is `__FoRtI1LiNk0__`). Before the
first change, back up the controller:

```text
FGT # execute backup config tftp fgt-pre-8-1-174.conf 10.30.99.50
```

### Lab 8.1 — DHCP snooping, trusted ports, option 82, and a rogue server

**Objective:** Show that a rogue DHCP server on an access port can answer
clients, enable DHCP snooping on `fsw-users`, confirm that the FortiGate's
server still works through the FortiLink trunk, read the binding database,
insert option 82, restrict replies to an allowed server list, and see the rogue
server's replies dropped.

**Platform notes:** Hands-on on C1, C2, and C3 with S1, S2, or S3 (on S3,
`FSW-A`): DHCP snooping, option 82, and the allowed server list are chain in
the 1xxE/1xxF and 200 Series columns (S1 and S2: at most 25 snooping VLANs,
note 15). After a C2 lab-VLAN NO-GO, run this lab on C1 or C3 or treat it as
read-and-predict. Track 2: the VLAN, global, and server-list settings run live;
the port settings run on the stand-in only with Lab 2.2's third outcome; the
switch and endpoint steps are read-and-predict.

**Track 1, Part A — the threat:**

1. Move endpoint B into `fsw-users` and give it the static rogue address:

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

2. Start a rogue DHCP server on endpoint B in the foreground. `--conf-file=/dev/null`
   ignores any `dnsmasq` configuration file, `--port=0` turns off its DNS
   server, and the pool and gateway are outside the real ones (`dnsmasq(8)`):

   ```bash
   # endpoint B
   sudo dnsmasq --no-daemon --conf-file=/dev/null --port=0 \
     --interface=<IFACE_B> --bind-interfaces \
     --dhcp-range=10.174.41.210,10.174.41.220,255.255.255.0,5m \
     --dhcp-option=3,10.174.41.20 --log-dhcp
   ```

3. Start `tcpdump` on endpoint A (Implementation and Automation), then bounce
   endpoint A's link. Predict how many OFFERs arrive and from whom.
   **Answer:** two, one from `10.174.41.1` with the FortiGate's MAC address and
   one from `10.174.41.20` with `<MAC_B>`; without snooping the switch forwards
   both. `dnsmasq` logs the DISCOVER and its OFFER. Record which lease endpoint A
   kept (`ip -br addr show <IFACE>`): whichever answer its client accepted first.
   Leave `dnsmasq` running.

**Track 1, Part B — snooping on:**

4. Read the switch's view before the change, and the FortiLink trunk's trust
   state:

   ```text
   FSW # get switch dhcp-snooping database-summary
   FSW # show switch interface <FL_TRUNK>
   ```

   Predict the trunk's `dhcp-snooping` line. **Answer:** the documentation does
   not say for the FortiLink trunk. Its examples of switch-formed trunks show
   `set dhcp-snooping trusted` (FortiLink Guide 7.6.7, p. 359), and a trunk
   that is not trusted would block the FortiGate's own replies once snooping is
   on. Record the line (a line that `show` omits is at its default,
   `untrusted`).

5. Enable snooping on the VLAN:

   ```text
   FGT # config system interface
   edit "fsw-users"
   set switch-controller-dhcp-snooping enable
   next
   end
   FGT # get switch-controller global
   ```

   In the `get` output, note `dhcp-snoop-client-req` (`drop-untrusted`),
   `dhcp-server-access-list` (`disable`), and the option 82 settings
   (`dhcp-option82-format ascii`, circuit ID `intfname vlan mode`, remote ID
   `mac`; FortiOS 7.6.0 CLI Reference).

6. Bounce endpoint A's link again with `tcpdump` running on A and `dnsmasq` on B.
   Predict both windows. **Answer:** endpoint A sees only the FortiGate's OFFER
   and leases an address from `.100`–`.199`; record it as `<LEASE_A>`.
   `dnsmasq` logs nothing at all: with `drop-untrusted`, the switch sends client
   broadcasts only to trusted ports, and `port2` is untrusted. If endpoint A gets
   no lease, the FortiLink trunk is not trusted (step 4); record that, disable
   snooping, and do the rest of this lab as read-and-predict.

7. Read the binding database from both sides. The controller command is from
   the FortiOS 8.0.1 CLI Reference (cross-check):

   ```text
   FGT # diagnose switch-controller switch-info dhcp-snooping database <SWITCH_SN>
   FSW # get switch dhcp-snooping client-db-details
   FSW # get switch dhcp-snooping server-db-details
   FSW # get switch dhcp-snooping database-summary
   ```

   Predict endpoint A's client entry and the server entries. **Answer:** a
   client row with `<MAC_A>`, VLAN 1741, `<LEASE_A>`, the lease time, and
   `port1` (the shape of the CLI Reference example, p. 494); a server row for
   the FortiGate on the FortiLink trunk, `trusted`. Whether the rogue appears
   depends on whether it has sent anything since snooping started; the negative
   test makes it send. Record the summary's count of snooping VLANs and its
   trusted and untrusted port lists.

**Track 1, Part C — option 82 and the allowed server list:**

8. Insert option 82 on `fsw-users`, renew endpoint A, and read the mapping. The
   guide gives the VLAN argument as `<VLAN_ID>` but its example uses a VLAN
   name; the FortiOS 8.0.1 reference calls it the managed FortiSwitch VLAN, a
   string. Try the interface name and record what your build accepts:

   ```text
   FGT # config system interface
   edit "fsw-users"
   set switch-controller-dhcp-snooping-option82 enable
   next
   end
   FGT # diagnose switch-controller switch-info option82-mapping snooping ascii <SWITCH_SN> fsw-users port1
   ```

   Predict the circuit ID. **Answer:** with the default `ascii` format, it is
   built from the interface name, VLAN, and mode (`intfname vlan mode`), and the
   remote ID from the MAC address (FortiLink Guide 7.6.7, p. 250). The
   documentation does not say how the FortiGate's own DHCP server treats a
   request with option 82 inserted by a snooping switch; record whether endpoint
   A still gets its lease, and check the server's view with `execute dhcp
   lease-list fsw-users` (FortiOS 8.0.1, cross-check).

9. Allow only the FortiGate as a server on `fsw-users`. The managed-switch
   entry's `dhcp-server-access-list` stays at `global`:

   ```text
   FGT # config switch-controller global
   set dhcp-server-access-list enable
   end
   FGT # config system interface
   edit "fsw-users"
   config dhcp-snooping-server-list
   edit "fgt-174"
   set server-ip 10.174.41.1
   next
   end
   next
   end
   FSW # get switch dhcp-snooping server-db-details
   ```

   Renew endpoint A. Predict the `svr-list` column for the FortiGate.
   **Answer:** `allowed`; a server not in the list shows `blocked` (CLI
   Reference, p. 494). Endpoint A still gets its lease. Record what the switch
   lists under `get switch dhcp-snooping allowed-sever-list` (the reference
   spells the syntax line that way and its example `allowed-server-list`; type
   `?` to see which your build takes).

**Track 2:** Run steps 5, 8 (the `config` block only), and 9 (the controller
blocks) on your controller; they are all live, and `show system interface
fsw-users` shows the result. If Lab 2.2's third outcome applies, also run step
1's block against `S248EPTF18000000`. Skip the endpoint and switch steps.

**Track 2: read-and-predict.**

1. The FortiSwitchOS 7.6.7 CLI Reference (pp. 494–495) prints this server
   database, trimmed:

   ```text
   FS1D243Z14000027 # get switch dhcp-snooping server-db-details
   mac vlan ip interface status svr-list last-seen-time expiry-time OFFER/ACK/NAK/OTHER
   00:11:01:00:00:01 10 xxx.x.x.x port1 trusted allowed 2018-09-11 11:21:09 2018-09-12 11:21:09 7/5/0/0
   ```

   Predict the row a rogue server on `port2` would add while the allowed list is
   on. **Answer:** the rogue's MAC address, VLAN 1741, `10.174.41.20`, `port2`,
   `untrusted`, and `blocked` in `svr-list` (a server not in the list), with its
   OFFER count.
2. The same reference prints a client database row ending in `port3`, and the
   Administration Guide marks a row `100.0.0.159*` (p. 283). Predict what the
   asterisk means. **Answer:** a temporary entry the server has not yet
   acknowledged; it becomes complete within 10 seconds or is removed.
3. A colleague enables snooping on 30 VLANs of an FS-124F. Predict the result.
   **Answer:** note 15 allows snooping on at most 25 VLANs on the FS-1xx
   models; record how FortiOS or the switch reports the excess if you ever try.

**Expected result:** Track 1: before snooping, endpoint A saw two OFFERs; with
snooping on, it sees only the FortiGate's and leases `<LEASE_A>`, `dnsmasq` sees
no DISCOVER, the binding database lists `<MAC_A>` on `port1`, the option 82
mapping and its effect on the lease are recorded, and the FortiGate is
`allowed` in the server list. Track 2: the VLAN, global, and server-list settings
were built, and the predictions are answered.

**Negative test:** Make the rogue answer and watch it fail. Send client
broadcasts to untrusted ports too, then capture on the FortiGate while endpoint
A renews. This is also the chapter's packet-capture exercise (exam task 4.1):
the sniffer runs on the controller, so it is Track 1 only, and its syntax is
from the FortiOS 8.0.1 CLI Reference (cross-check):

```text
FGT # config switch-controller global
set dhcp-snoop-client-req forward-untrusted
end
FGT # diagnose sniffer packet fsw-users 'udp port 67 or udp port 68' 4 20
```

Bounce endpoint A's link while the sniffer runs. Predict three things.
**Answer:** `dnsmasq` now logs the DISCOVER and sends an OFFER; endpoint A's
`tcpdump` and the FortiGate's sniffer show only the FortiGate's OFFER, because
the switch drops server messages at the untrusted `port2`; and `get switch
dhcp-snooping server-db-details` lists the rogue on `port2` as `untrusted` and
`blocked`. Look for the rogue-server log message on the switch with `execute log
display` and record whether it appears. Track 2: prediction 1 is the negative
test.

**Rollback:** Stop `dnsmasq` with Ctrl+C, then return the VLAN, the global
settings, and `port2`:

```text
FGT # config system interface
edit "fsw-users"
config dhcp-snooping-server-list
delete "fgt-174"
end
set switch-controller-dhcp-snooping-option82 disable
set switch-controller-dhcp-snooping disable
next
end
FGT # config switch-controller global
set dhcp-server-access-list disable
set dhcp-snoop-client-req drop-untrusted
end
FGT # config switch-controller managed-switch
edit <SWITCH_SN>
config ports
edit "port2"
set vlan "fsw-iot"
next
end
next
end
```

```bash
# endpoint B
sudo ip addr del 10.174.41.20/24 dev <IFACE_B>
ping -c 3 10.174.43.1
```

Bounce endpoint A's link and confirm a lease from `.100`–`.199` and a ping to
`10.174.41.1`. `dnsmasq` stays disabled on endpoint B.

**Lab verified by:** *pending*

### Lab 8.2 — Dynamic ARP inspection and IP source guard

**Objective:** Spoof an ARP binding without DAI and see the FortiGate accept it,
enable DAI on `fsw-users` and see a spoofed ARP packet dropped and counted,
admit statically addressed endpoint B with a DHCP-snooping static entry, and,
on S3, filter spoofed source addresses with IP source guard.

**Platform notes:** Part A (DAI) is hands-on on C1, C2, and C3 with S1, S2, or
S3 (on S3, `FSW-A`): DAI is chain in both columns. Part B (IP source guard) is
hands-on only on S3; on S1 and S2 it is not supported (matrix dash), and step 8
only records whether FortiOS accepts the setting. After a C2 lab-VLAN NO-GO,
use C1 or C3 or read-and-predict. Track 2: the VLAN settings run live; the
static entry and the port settings run on the stand-in only with Lab 2.2's
third outcome (the FS-248E-POE stand-in is a 200 Series model, which supports IP
source guard); the rest is read-and-predict.

**Track 1, Part A — DAI:**

1. Turn snooping back on (DAI needs it, prerequisite P12 in Volume CLXXII),
   renew endpoint A, and confirm its binding:

   ```text
   FGT # config system interface
   edit "fsw-users"
   set switch-controller-dhcp-snooping enable
   next
   end
   FSW # get switch dhcp-snooping client-db-details
   ```

   Bounce endpoint A's link first, so the switch sees a fresh exchange; the row
   must show `<MAC_A>`, VLAN 1741, `<LEASE_A>` (record it again if it changed),
   and `port1`.

2. Without DAI, claim an address that was never leased. Add it to endpoint A,
   send ARP from it, and read the FortiGate's ARP table (`diagnose ip arp list`,
   FortiOS 8.0.1, cross-check):

   ```bash
   # endpoint A
   sudo ip addr add 10.174.41.50/24 dev <IFACE>
   sudo arping -c 3 -I <IFACE> -s 10.174.41.50 10.174.41.1
   sudo ip addr del 10.174.41.50/24 dev <IFACE>
   ```

   ```text
   FGT # diagnose ip arp list
   ```

   Predict the result. **Answer:** `arping` gets three replies, and the
   FortiGate lists `10.174.41.50` with `<MAC_A>`: nothing checks that endpoint A
   owns that address.

3. Read the FortiLink trunk's ARP trust, then enable DAI:

   ```text
   FSW # show switch interface <FL_TRUNK>
   FGT # config system interface
   edit "fsw-users"
   set switch-controller-arp-inspection enable
   next
   end
   ```

   Predict the trunk's `arp-inspection-trust`. **Answer:** the documentation
   does not say for the FortiLink trunk; the switch default is `untrusted` (CLI
   Reference, `config switch interface`). Record the line. Then test the
   gateway from endpoint A's real address:

   ```bash
   # endpoint A
   sudo ip neigh flush dev <IFACE>
   ping -c 3 10.174.41.1
   ```

   If the ping fails, the FortiGate's ARP replies are being dropped on the
   trunk: record it, set `switch-controller-arp-inspection disable`, and do
   steps 4 and 5 as read-and-predict.

4. Spoof again, with a new address so that the FortiGate's old entry for `.50`
   does not confuse the result, and read the statistics. The controller command
   is the FortiLink Guide's (p. 252); the switch command is the Administration
   Guide's (p. 288), matched by hand:

   ```bash
   # endpoint A
   sudo ip addr add 10.174.41.51/24 dev <IFACE>
   sudo arping -c 3 -I <IFACE> -s 10.174.41.51 10.174.41.1
   sudo ip addr del 10.174.41.51/24 dev <IFACE>
   ```

   ```text
   FGT # diagnose switch-controller switch-info arp-inspection stats <SWITCH_SN>
   FSW # diagnose switch arp-inspection stats
   FGT # diagnose ip arp list
   ```

   Predict the counters and the ARP table. **Answer:** `arping` gets no reply;
   the `dropped` row for VLAN 1741 counts endpoint A's three ARP requests (the
   shape of the Administration Guide's example: `received`, `forwarded`, and
   `dropped` rows with `arp-request` and `arp-reply` columns); and the FortiGate
   has no entry for `10.174.41.51`. Endpoint A's real address still works.

5. Admit a static host. Put endpoint B in `fsw-users` with its static address,
   test it, add a static entry, and test again:

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

   Predict the ping. **Answer:** it fails: endpoint B's address is static, so it
   has no binding, and DAI drops its ARP requests. Add the entry; the FortiOS
   7.6.0 reference describes `vlan` as a VLAN name, while the guide's example
   uses an ID (p. 254), so if FortiOS rejects the name, enter `1741` and record
   which form it took:

   ```text
   FGT # config switch-controller managed-switch
   edit <SWITCH_SN>
   config dhcp-snooping-static-client
   edit "ep-b-174"
   set vlan "fsw-users"
   set ip 10.174.41.20
   set mac <MAC_B>
   set port "port2"
   next
   end
   next
   end
   FSW # get switch dhcp-snooping static-clients
   ```

   Repeat endpoint B's ping. It now succeeds, and the static client list shows
   the entry with the `*` (static) marker and `Infinity` lease, the shape of the
   CLI Reference example (p. 495).

**Track 1, Part B — IP source guard (S3):**

6. Turn DAI off but keep snooping, so that only IP source guard is tested, and
   enable IP source guard on `port1`:

   ```text
   FGT # config system interface
   edit "fsw-users"
   set switch-controller-arp-inspection disable
   next
   end
   FGT # config switch-controller managed-switch
   edit <SWITCH_SN>
   config ports
   edit "port1"
   set ip-source-guard enable
   next
   end
   next
   end
   ```

7. Read the entries from both sides and test a spoofed source:

   ```text
   FGT # diagnose switch-controller switch-info ip-source-guard hardware <SWITCH_SN>
   FSW # diagnose switch ip-source-guard hardware entry list
   FSW # get switch ip-source-guard
   ```

   ```bash
   # endpoint A
   ping -c 3 10.174.41.1
   sudo ip addr add 10.174.41.52/24 dev <IFACE>
   ping -c 3 -I 10.174.41.52 10.174.41.1
   ```

   Predict the entries and the two pings. **Answer:** a dynamic entry for
   `<LEASE_A>` and `<MAC_A>` on `port1`, learned by DHCP snooping (FortiLink
   Guide 7.6.7, p. 256); the ping from `<LEASE_A>` succeeds and the ping from
   `.52` fails, because its source address has no binding. The guide says
   IP source guard filters IPv4 traffic and does not say whether ARP from an
   unbound address is affected; record whether the FortiGate learned `.52` in
   `diagnose ip arp list`.

8. Bind `.52` statically and repeat the spoofed ping:

   ```text
   FGT # config switch-controller managed-switch
   edit <SWITCH_SN>
   config ip-source-guard
   edit "port1"
   config binding-entry
   edit "1"
   set ip 10.174.41.52
   set mac <MAC_A>
   next
   end
   next
   end
   next
   end
   ```

   The ping from `.52` now succeeds: static entries are allowed sources, and win
   over dynamic ones in a conflict (p. 254). The guide does not define a
   conflict; repeat the ping from `<LEASE_A>` and record whether a static entry
   for `<MAC_A>` displaced the dynamic one. On **S1 and S2**, run only step 6's
   `set ip-source-guard enable` and record whether FortiOS refuses it (the guide
   says it can be configured only for switches that support it) or accepts it
   without the switch enforcing anything; then unset it.

**Track 2:** Run steps 1 and 3's `config system interface` blocks on your
controller and check them with `show system interface fsw-users`. If Lab 2.2's
third outcome applies, also run step 5's static-entry block (with `port2` as
the port) and steps 6 and 8's managed-switch blocks against
`S248EPTF18000000`, and check them with `show switch-controller managed-switch
S248EPTF18000000`. Skip the endpoint and switch steps.

**Track 2: read-and-predict.**

1. The Administration Guide (p. 288) prints DAI statistics in this shape:

   ```text
   vlan 100 arp-request arp-reply
   received 0 0
   forwarded 0 0
   dropped 0 0
   ```

   A host on an untrusted port sends three ARP requests with a sender address it
   never leased, then three with its own leased address. Predict the rows.
   **Answer:** `received` 6 under `arp-request`, `forwarded` 3, `dropped` 3; the
   replies the FortiGate sends come in over the trunk and are counted only if
   the trunk is untrusted.
2. FortiOS 7.6.4 and later can log IP source-guard violations; the FortiLink
   Guide (p. 256) prints:

   ```text
   Timestamp | Interface | IP | MAC
   2025-06-02 17:19:36 | port23 | 0.1.2.3 | 00:11:22:aa:bb:cc
   ```

   Predict how many entries one noisy port can fill. **Answer:** at most 5 per
   port and 128 in all, values that cannot be changed; the log covers all
   switches in the VDOM (p. 256). FGT-1 runs 7.6.2, so this is read-only here.
3. An administrator adds a DHCP-snooping static entry on `port2`, then tries to
   move `port2` into a trunk. Predict the result. **Answer:** refused until the
   entry is deleted (p. 253).

**Expected result:** Track 1: without DAI, the FortiGate accepted a spoofed
binding; with DAI, endpoint A's spoofed ARP was dropped and counted while its
real address kept working, and the trunk's ARP trust is recorded; endpoint B's
static address worked only after its static entry; on S3, IP source guard passed
`<LEASE_A>` and dropped `.52` until it was bound; on S1 or S2, FortiOS's
response to IP source guard is recorded. Track 2: the VLAN settings (and the
stand-in's entries, if accepted) were built, and the predictions are answered.

**Negative test:** Try DAI on a VLAN without snooping. `fsw-iot` has none:

```text
FGT # config system interface
edit "fsw-iot"
set switch-controller-arp-inspection enable
next
end
```

Predict and record the result. **Answer:** the switch side requires snooping
first (FortiSwitchOS 7.6.7 CLI Reference, p. 186); the FortiOS 7.6.0 reference
states no such dependency, so FortiOS may refuse the setting or accept it with
no effect on the switch. Record which, check the switch with `show switch vlan
1743`, and then `set switch-controller-arp-inspection disable` on `fsw-iot`.
Track 2: run the same block and record FortiOS's response.

**Rollback:** Delete the static entries **first**: with the DHCP-snooping
entry in place, `fsw-users` cannot be removed from `port2`.

```text
FGT # config switch-controller managed-switch
edit <SWITCH_SN>
config dhcp-snooping-static-client
delete "ep-b-174"
end
config ip-source-guard
delete "port1"
end
config ports
edit "port1"
set ip-source-guard disable
next
edit "port2"
set vlan "fsw-iot"
next
end
next
end
FGT # config system interface
edit "fsw-users"
set switch-controller-arp-inspection disable
set switch-controller-dhcp-snooping disable
next
end
```

On S1 and S2, the `config ip-source-guard` and `ip-source-guard` lines do not
apply; leave them out.

```bash
# endpoint A
sudo ip addr del 10.174.41.52/24 dev <IFACE>
# endpoint B
sudo ip addr del 10.174.41.20/24 dev <IFACE_B>
ping -c 3 10.174.43.1
```

Bounce endpoint A's link and confirm its lease and a ping to `10.174.41.1`.

**Lab verified by:** *pending*

### Lab 8.3 — Storm control

**Objective:** Read the global, per-switch, and per-port storm-control
settings, measure a broadcast flood from endpoint A with and without a
storm-control policy on `port1`, and see the `disabled` mode and a rate of 0 at
work.

**Platform notes:** Hands-on on C1, C2, and C3 with S1, S2, or S3 (on S3,
`FSW-A`): storm control and per-port storm control are chain in both columns;
on S1 and S2 the switch has no `storm-control-high-rate` or
`storm-control-rate-filter` (note 21), and storm-control monitoring is a
standalone feature everywhere. `burst-size-level` needs FortiOS 7.6.4 and is
not used. After a C2 lab-VLAN NO-GO, use `video` with static addresses (Design
Considerations). Track 2: the policy and the global read run live; applying the
policy to a port runs on the stand-in only with Lab 2.2's third outcome; the
measurements are read-and-predict.

**Track 1:**

1. Read the three levels and the switch's view. `get` prints every field:

   ```text
   FGT # get switch-controller storm-control
   FGT # show switch-controller storm-control-policy
   FGT # show switch-controller managed-switch <SWITCH_SN>
   FSW # get switch storm-control
   FSW # show switch physical-port port1
   ```

   Predict the global values and `port1`'s storm control. **Answer:** rate 500
   with `broadcast`, `unknown-unicast`, and `unknown-multicast` all `disable`
   (FortiOS 7.6.0 CLI Reference); the managed-switch entry's `config
   storm-control` at its defaults, `local-override disable` (a line that `show`
   omits is at its default); and `port1` with no storm control in effect. Record whether `show
   switch-controller storm-control-policy` lists a policy named `default` (the
   7.6.0 reference's default value for a port's `storm-control-policy`) and its
   mode. Do not enable global storm control in this lab: it also applies to the
   FortiLink ports (FortiLink Guide 7.6.7, p. 145).

2. Put endpoint B in `fsw-users` as the receiver, then measure a flood without
   storm control. On endpoint B, start a 15-second capture that counts
   broadcast pings; on endpoint A, send 2,000 of them at 200 per second (10
   seconds; `-b` allows a broadcast destination):

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
   sudo timeout -s INT 15 tcpdump -ni <IFACE_B> -w /dev/null 'icmp and dst host 10.174.41.255'
   ```

   ```bash
   # endpoint A (start within a few seconds of endpoint B's capture)
   sudo ping -b -q -i 0.005 -c 2000 10.174.41.255
   ```

   Predict the `packets captured` line on endpoint B. **Answer:** about 2,000;
   nothing limits broadcast. Record the number as the baseline.

3. Create a policy that limits broadcast to 50 packets per second and apply it
   to `port1`, where the flood enters:

   ```text
   FGT # config switch-controller storm-control-policy
   edit "storm-174"
   set description "Lab 8.3 broadcast limit"
   set storm-control-mode override
   set rate 50
   set broadcast enable
   set unknown-unicast disable
   set unknown-multicast disable
   next
   end
   FGT # config switch-controller managed-switch
   edit <SWITCH_SN>
   config ports
   edit "port1"
   set storm-control-policy "storm-174"
   next
   end
   next
   end
   FSW # show switch physical-port port1
   ```

   Predict what the switch shows. **Answer:** `storm-control-mode override` and
   a `config storm-control` block with `broadcast enable` and `rate 50`, the
   per-port form of the Administration Guide (p. 360). The FortiLink Guide does
   not show the pushed result, so record the lines your switch prints.

4. Repeat step 2's capture and flood. Predict the count. **Answer:** roughly
   50 per second for 10 seconds, about 500, plus whatever burst the hardware
   allows; record the exact number. Then read the switch's drop view:

   ```text
   FSW # diagnose switch storm-control
   ```

   The CLI Reference's FS-124E example shows `storm-control-monitor enabled`
   and a per-port drop list (pp. 378–379); storm-control monitoring is marked
   standalone-only in the matrix, so record what your managed switch prints.

5. Switch the policy to `disabled` and repeat the measurement:

   ```text
   FGT # config switch-controller storm-control-policy
   edit "storm-174"
   set storm-control-mode disabled
   next
   end
   ```

   Predict the count. **Answer:** about 2,000 again: `disabled` turns storm
   control off on the port whatever the global and switch-level settings are
   (FortiOS 7.6.0 CLI Reference). Set `storm-control-mode override` again.

**Track 2:** Run step 1's controller commands and step 3's policy block on your
controller and check the policy with `show switch-controller
storm-control-policy storm-174`. If Lab 2.2's third outcome applies, also apply
it to the stand-in's `port1` (step 3's second block against
`S248EPTF18000000`). Skip the endpoint and switch steps.

**Track 2: read-and-predict.**

1. The CLI Reference (p. 510) prints:

   ```text
   S524DF4K15000024 # get switch storm-control
   broadcast : enable
   rate : 1000
   unknown-multicast : enable
   unknown-unicast : enable
   ```

   Predict which FortiOS command produced these values on a managed switch.
   **Answer:** the global `config switch-controller storm-control` (or the
   switch's `config storm-control` with `local-override enable`); a per-port
   policy appears under `config switch physical-port` instead.
2. An administrator sets the global rate to 0 with `broadcast enable` to stop
   a storm. Predict the side effect. **Answer:** every port of every managed
   switch, FortiLink ports included, drops all broadcast traffic, so ARP and
   DHCP stop working everywhere (a rate of 0 drops all packets of the enabled
   types, p. 144).
3. Predict whether `set burst-size-level 2` works under `config
   switch-controller storm-control` on FGT-1. **Answer:** no; the option is from
   FortiOS 7.6.4 (p. 145) and is not in the 7.6.0 reference.

**Expected result:** Track 1: the defaults matched; the baseline count was about
2,000; with `storm-174` on `port1` the count dropped to roughly 500 (your number
recorded); `disabled` restored the full flood; the switch's per-port settings
and its `diagnose switch storm-control` output are recorded. Track 2: the
policy was built (and applied to the stand-in, if accepted), and the
predictions are answered.

**Negative test:** Set the rate to 0 and show that it also stops ARP:

```text
FGT # config switch-controller storm-control-policy
edit "storm-174"
set rate 0
next
end
```

```bash
# endpoint A
sudo ip neigh flush dev <IFACE>
ping -c 3 10.174.41.1
```

Predict and observe: the ping fails, because endpoint A's ARP request for its
gateway is a broadcast and every broadcast entering `port1` is dropped. Set
`rate 50` again (or go straight to the rollback). Track 2: prediction 2 is the
negative test.

**Rollback:**

```text
FGT # config switch-controller managed-switch
edit <SWITCH_SN>
config ports
edit "port1"
unset storm-control-policy
next
edit "port2"
set vlan "fsw-iot"
next
end
next
end
FGT # config switch-controller storm-control-policy
delete "storm-174"
end
```

```bash
# endpoint B
sudo ip addr del 10.174.41.20/24 dev <IFACE_B>
ping -c 3 10.174.43.1
```

Confirm with `show switch physical-port port1` that the per-port storm control
is gone and that endpoint A reaches `10.174.41.1`.

**Lab verified by:** *pending*

### Lab 8.4 — ACLs in FortiLink mode

**Objective:** Build an ACL ingress policy and an ACL group, apply the group to
`port1`, count and then drop endpoint A's traffic to its gateway, and show that
an ingress ACL acts only on the port where traffic arrives.

**Platform notes:** Hands-on only on S3 (`FSW-A`), with C1, C2, or C3: ingress
ACLs are chain in the 200 Series column. On S1 and S2 there is no ACL in
FortiLink mode (note 16): build the objects, run step 2 only to record how
FortiOS responds, read the rest, and do the hands-on ACL work in Lab 11.4 with
the switch in standalone mode. After a C2 lab-VLAN NO-GO, use `video` and 4090
(Design Considerations). Track 2: the ACL objects run live; binding the group to
a port runs on the stand-in only with Lab 2.2's third outcome (its FS-248E-POE
model is a 200 Series switch, not listed in note 16); the counters are
read-and-predict.

**Track 1:**

1. Read the switch's ACL state before the change:

   ```text
   FSW # get switch acl usage
   FSW # get switch acl ingress
   ```

   Record the free ingress rules and counters (the `RULES` and `COUNTERS`
   columns of the CLI Reference example, p. 493) and whether any ingress ACL is
   present already (features of the switch can install their own).

2. Create a counting ACL for endpoint A's traffic to its gateway, put it in a
   group, and apply the group to `port1`:

   ```text
   FGT # config switch-controller acl ingress
   edit 1
   set description "lab-174 to gateway"
   config action
   set count enable
   set drop disable
   end
   config classifier
   set dst-ip-prefix 10.174.41.1 255.255.255.255
   set vlan 1741
   end
   next
   end
   FGT # config switch-controller acl group
   edit "acl-174"
   set ingress 1
   next
   end
   FGT # config switch-controller managed-switch
   edit <SWITCH_SN>
   config ports
   edit "port1"
   set acl-group "acl-174"
   next
   end
   next
   end
   ```

   On S1 or S2, record whether FortiOS accepts `set acl-group` on `port1`; the
   guide says a switch without ACL group 3 does not support user ACLs (p. 258),
   and the switch will not enforce them either way. Then skip to the rollback.

3. Send ten pings and read the counters from both sides. The controller command
   is the FortiLink Guide's form (p. 259); the FortiOS 8.0.1 reference adds a
   port argument, so if your build asks for one, add `port1`:

   ```bash
   # endpoint A
   ping -c 10 10.174.41.1
   ```

   ```text
   FGT # diagnose switch-controller switch-info acl-counters <SWITCH_SN>
   FSW # get switch acl ingress
   FSW # get switch acl counters ingress
   ```

   Predict the packet counter and where the ACL sits on the switch.
   **Answer:** at least 10 packets (the ICMP echo requests; ARP has no IP header,
   so the IP classifier does not match it), with the pings all answered; on the
   switch the ACL appears as an ingress entry in **group 3**, where the
   controller's ingress policies go (p. 258), on `port1`. The 200 Series has
   byte counters; the FS-1xxE, FS-1xxF, and FS-4xxE always show 0 bytes
   (p. 259).

4. Turn the ACL into a drop rule and repeat the pings:

   ```text
   FGT # config switch-controller acl ingress
   edit 1
   config action
   set drop enable
   end
   next
   end
   ```

   Predict the pings and the counter. **Answer:** all ten pings fail, and the
   counter keeps rising, because `count` stays enabled. Other traffic from
   endpoint A (for example its DHCP renewals and ARP) is unaffected: the
   classifier matches only IPv4 packets to `10.174.41.1/32` in VLAN 1741.

**Track 2:** Run step 2's first two blocks on your controller and check them
with `show switch-controller acl ingress` and `show switch-controller acl
group`. If Lab 2.2's third outcome applies, also run step 2's third block
against `S248EPTF18000000` and check it with `show switch-controller
managed-switch S248EPTF18000000`. Skip the endpoint and switch steps.

**Track 2: read-and-predict.**

1. The CLI Reference (p. 493) prints:

   ```text
   S524DF4K15000024 # get switch acl counters ingress
   ingress:
   ID Packets Bytes description
   0001 0 0 cnt_n_mirror13
   0002 0 0 cnt_n_mirror31
   ```

   After ten dropped pings through a `count` and `drop` ACL on an FS-124F in
   **standalone** mode, predict the `Packets` and `Bytes` columns. **Answer:**
   `Packets` 10 and `Bytes` 0: the FS-1xxF has no ACL byte counters (FortiLink
   Guide 7.6.7, p. 259), and on that model the ACL exists only in standalone
   mode (note 16).
2. The FortiLink Guide's configuration example (pp. 259–260) blocks a PC
   with source MAC `00:0c:29:d4:4f:3c` from reaching `8.8.8.8/32`, applied to
   `port6` of an FS-248E-POE. Predict whether the same group applied to the
   switch's FortiLink trunk instead would block that PC. **Answer:** no; an
   ingress ACL acts on traffic arriving on the port it is applied to, and the
   PC's traffic arrives on `port6`.
3. A colleague wants an egress ACL on `FSW-A` in FortiLink mode. Predict the
   answer. **Answer:** not available: FortiLink mode supports only the ingress
   stage (note 16), and the matrix marks egress and prelookup ACLs as not
   supported in the 200 Series column even in standalone mode.

**Expected result:** Track 1 (S3): ACL 1 in group `acl-174` on `port1` counted
endpoint A's pings, then dropped them while counting; the switch showed the
entry in group 3; the free TCAM before the change is recorded. S1 and S2:
FortiOS's response to `acl-group` is recorded. Track 2: the ACL objects were
built (and bound to the stand-in, if accepted), and the predictions are answered.

**Negative test:** Move the group from `port1` to `port2`:

```text
FGT # config switch-controller managed-switch
edit <SWITCH_SN>
config ports
edit "port1"
unset acl-group
next
edit "port2"
set acl-group "acl-174"
next
end
next
end
```

Predict and observe: endpoint A's pings to `10.174.41.1` succeed again, because
they enter on `port1`; endpoint B (still in `fsw-iot`, pinging `10.174.43.1`)
is unaffected too, because its traffic does not match the classifier. Track 2:
prediction 2 is the negative test.

**Rollback:**

```text
FGT # config switch-controller managed-switch
edit <SWITCH_SN>
config ports
edit "port1"
unset acl-group
next
edit "port2"
unset acl-group
next
end
next
end
FGT # config switch-controller acl group
delete "acl-174"
end
FGT # config switch-controller acl ingress
delete 1
end
```

Confirm with `get switch acl ingress` on the switch that the entry is gone, and
that endpoint A reaches `10.174.41.1`.

**Lab verified by:** *pending*

### Lab 8.5 — Intra-VLAN blocking, native VLAN hygiene, and private VLANs

**Objective:** Block host-to-host traffic in `fsw-users`, let two hosts talk
again only through the FortiGate (proxy ARP, `allow-traffic-redirect disable`,
and policy P3), apply native VLAN hygiene to an access port and an unused port,
predict private VLAN behavior, and map this chapter's controls to the Volume
CLXXII hardening requirements.

**Platform notes:** Parts A and B are hands-on on C1, C2, and C3 with S1, S2,
or S3 (on S3, `FSW-A`): blocking intra-VLAN traffic is chain in both columns
(note 7: at most 16 access VLANs on the FS-108F and FS-124F, which this lab adds
one to). On C2, Part A uses P3, the last free policy slot, and deletes it; if
Lab 4.1 already used P3, step 7 is read-and-predict there. After a C2 lab-VLAN
NO-GO, Part A needs C1 or C3. Part C (private VLANs) is read-and-predict on
every option: not supported on S1 and S2, standalone-only on S3 (Chapter 11
runs the switch standalone). Part D is a mapping exercise. Track 2: the VLAN,
proxy ARP, global, and policy settings run live; the port settings run on the
stand-in only with Lab 2.2's third outcome; the endpoint and switch steps are
read-and-predict.

**Track 1, Part A — block, then allow through the FortiGate:**

1. Put endpoint B in `fsw-users` (as in Lab 8.3 step 2, with `10.174.41.20/24`
   on `<IFACE_B>`) and test host to host:

   ```bash
   # endpoint A
   ping -c 3 10.174.41.20
   ip neigh show 10.174.41.20
   ```

   The ping works and the neighbor entry shows `<MAC_B>`: the switch forwards
   between `port1` and `port2` directly.

2. Record the FortiGate's `allow-traffic-redirect` value (the 7.6.0 default is
   `enable`), then block intra-VLAN traffic:

   ```text
   FGT # get system global
   FGT # config system interface
   edit "fsw-users"
   set switch-controller-access-vlan enable
   next
   end
   ```

3. Test again from a clean neighbor table:

   ```bash
   # endpoint A
   sudo ip neigh flush dev <IFACE>
   ping -c 3 10.174.41.20
   ip neigh show 10.174.41.20
   ping -c 3 10.174.41.1
   ```

   Predict both pings and the neighbor entry. **Answer:** the ping to endpoint B
   fails and its neighbor entry is `INCOMPLETE` or `FAILED`: endpoint A's ARP
   broadcast now reaches only the FortiGate, which does not answer for an
   address that is not its own. The ping to the gateway works: hosts can still
   reach the FortiGate (FortiLink Guide 7.6.7, p. 261).

4. Let the FortiGate answer ARP for the two hosts, and no others: one entry
   for endpoint B and one for endpoint A's lease (`end-ip` is optional). Do not
   renew endpoint A's lease while entry 2 exists; a DHCP client that probes its
   new address with ARP would get the FortiGate's answer and could decline the
   lease:

   ```text
   FGT # config system proxy-arp
   edit 1
   set interface "fsw-users"
   set ip 10.174.41.20
   next
   edit 2
   set interface "fsw-users"
   set ip <LEASE_A>
   next
   end
   ```

5. With `allow-traffic-redirect` still at its recorded value, flush and test:

   ```bash
   # endpoint A
   sudo ip neigh flush dev <IFACE>
   ping -c 3 10.174.41.20
   ip neigh show 10.174.41.20
   ```

   Predict the neighbor entry, then record the ping. **Answer:** the entry now
   shows the FortiGate's MAC address, not `<MAC_B>`, so the echo requests go to
   the FortiGate. Whether they come back depends on `allow-traffic-redirect`: the
   7.6.0 reference describes the enabled setting as forwarding traffic with the
   same ingress and egress interface without a policy check, and the guide
   requires it disabled for intra-VLAN blocking (p. 261). If the value is
   `enable` and the ping succeeds, that is the unchecked redirect; record the
   result either way.

6. Disable the redirect and test again:

   ```text
   FGT # config system global
   set allow-traffic-redirect disable
   end
   ```

   Repeat step 5's ping. Predict the result. **Answer:** it fails: the traffic
   now needs a firewall policy, and none allows `fsw-users` to `fsw-users`.

7. Allow ping between `fsw-users` hosts with P3. The policy uses the zone,
   because `fsw-users` is a member of `FSW-LAN` and FortiOS configures policies
   for the zone instead of its member interfaces (FortiOS 7.6.0 CLI Reference,
   `config system zone`); the address object keeps it to `fsw-users`:

   ```text
   FGT # config firewall address
   edit "fsw-users-net-174"
   set subnet 10.174.41.0 255.255.255.0
   next
   end
   FGT # config firewall policy
   edit 0
   set name "P3-intravlan-174"
   set srcintf "FSW-LAN"
   set dstintf "FSW-LAN"
   set srcaddr "fsw-users-net-174"
   set dstaddr "fsw-users-net-174"
   set action accept
   set schedule "always"
   set service "PING"
   set logtraffic all
   next
   end
   FGT # show firewall policy
   ```

   Record the new policy's ID as `<P3_ID>`. Repeat the ping from endpoint A to
   `10.174.41.20` while the FortiGate captures (FortiOS 8.0.1, cross-check):

   ```text
   FGT # diagnose sniffer packet fsw-users 'icmp' 4 8
   ```

   Predict the capture. **Answer:** each echo request appears twice on
   `fsw-users`, once arriving from endpoint A and once leaving toward endpoint
   B, and each reply likewise: the FortiGate is now the path between the two
   hosts, under P3.

8. Read the setting that decides what the switch does if it loses the
   FortiGate:

   ```text
   FGT # show switch-controller fortilink-settings
   ```

   Predict `access-vlan-mode`. **Answer:** `legacy`, the default (FortiLink
   Guide 7.6.7, p. 263); `fail-open` would let hosts in an access VLAN talk
   directly while FortiLink is down, `fail-close` would keep them apart. Leave
   it unchanged.

**Track 1, Part B — native VLAN hygiene:**

9. Audit the ports' native VLANs:

   ```text
   FGT # show switch-controller managed-switch <SWITCH_SN>
   ```

   Predict which front ports still have `<DEFAULT_VLAN>` as their native VLAN.
   **Answer:** every front port the labs have not changed: `port3`, `port4`,
   `port5`, `port6`, and the unused ports above them, apart from
   `<FSW_FL_PORT>` (`port1` and, for now, `port2` are in `fsw-users`); a line
   that `show` omits is at its default. Those are the ports the Volume CLXXII crosswalk rules
   `CISC-L2-000210` and `CISC-L2-000220` care about.

10. Shut an unused port and mark it. `port4` is unused on every switch option
    (`port3` may carry management in Chapter 11, and `port7` can be the
    FortiLink port on an FS-108F):

    ```text
    FGT # config switch-controller managed-switch
    edit <SWITCH_SN>
    config ports
    edit "port4"
    set description "unused-174"
    set status down
    next
    end
    next
    end
    FSW # diagnose switch physical-ports summary port4
    ```

    The summary (its port argument is optional, matched by hand) shows `port4`
    administratively down. A parking VLAN with no gateway, the other half of
    `CISC-L2-000210`, would cost an interface on C2; on C1 and C3 it is a design
    choice this volume does not make.

11. Make `port1` a strict access port: discard tagged frames, as
    `CISC-L2-000250`'s FortiSwitch setting does (`discard-mode all-tagged`):

    ```text
    FGT # config switch-controller managed-switch
    edit <SWITCH_SN>
    config ports
    edit "port1"
    set discard-mode all-tagged
    next
    end
    next
    end
    ```

    ```bash
    # endpoint A
    ping -c 3 10.174.41.1
    ```

    Endpoint A sends untagged frames, so the ping still works. Record it: the
    documentation does not say how `discard-mode` interacts with the tagged
    VLANs in `port1`'s allowed list (`quarantine`); Chapter 09's quarantine lab
    needs the port back at `none`, which the rollback restores.

**Track 1, Part C — private VLANs (read-and-predict):**

12. The Administration Guide (p. 356) configures a private VLAN on a standalone
    switch like this, trimmed (switch-side syntax; not run in FortiLink mode):

    ```text
    config switch vlan
    edit 1000
    set private-vlan enable
    set isolated-vlan 101
    set community-vlans 200-210
    end
    config switch interface
    edit "port2"
    set private-vlan promiscuous
    set primary-vlan 1000
    next
    edit "port3"
    set private-vlan sub-vlan
    set primary-vlan 1000
    set sub-vlan 200
    next
    edit "port7"
    set private-vlan sub-vlan
    set primary-vlan 1000
    set sub-vlan 101
    next
    edit "port20"
    set private-vlan sub-vlan
    set primary-vlan 1000
    set sub-vlan 101
    end
    ```

    Predict which pairs can exchange traffic: `port7` and `port20`; `port3` and
    `port7`; `port3` and `port2`. **Answer:** `port7` and `port20` cannot (both
    in the isolated VLAN 101, whose hosts cannot reach each other); `port3` and
    `port7` cannot (different secondary VLANs); `port3` and `port2` can (a
    community port reaches the promiscuous port). Compare intra-VLAN blocking
    in Part A: there every host is effectively isolated and the FortiGate is the
    only "promiscuous" peer, and policy decides exceptions.

**Track 1, Part D — mapping to the Volume CLXXII requirements:**

13. Fill in the last column from your results. The rules and SRG IDs are from
    [Volume CLXXII, Chapter 33](../../volume-172-disa-srgs-and-stigs/chapters/33-fortiswitch-and-cisco-catalyst-switch-stig-crosswalk.md)
    (Chapter 37 aligns the NX-OS rules the same way); that crosswalk gives the
    **standalone** FortiSwitchOS commands, and the middle column gives this
    chapter's FortiLink-mode equivalent:

    | Rule (SRG ID) | Requirement | FortiLink-mode setting in this chapter | Your evidence |
    | --- | --- | --- | --- |
    | `CISC-L2-000120` (`SRG-NET-000362-L2S-000024`) | Block unknown unicast flooding on host ports | A storm-control policy with only `unknown-unicast` enabled and `rate 0` (Lab 8.3's policy form) | |
    | `CISC-L2-000130` (`SRG-NET-000362-L2S-000025`) | DHCP snooping on user VLANs | `switch-controller-dhcp-snooping enable`; trusted FortiLink trunk (Lab 8.1) | |
    | `CISC-L2-000140` (`SRG-NET-000362-L2S-000026`) | IP source guard on host ports | `ip-source-guard enable` (Lab 8.2, S3 only; P9, P14) | |
    | `CISC-L2-000150` (`SRG-NET-000362-L2S-000027`) | DAI on user VLANs | `switch-controller-arp-inspection enable` after snooping (Lab 8.2; P12) | |
    | `CISC-L2-000160` (`SRG-NET-000512-L2S-000001`) | Storm control on host ports | `storm-control-policy` on each host port (Lab 8.3) | |
    | `CISC-L2-000210` (`SRG-NET-000512-L2S-000007`) | Disabled ports in an unused VLAN | `status down` (Lab 8.5 step 10); parking VLAN not built | |
    | `CISC-L2-000220`, `CISC-L2-000270` (`SRG-NET-000512-L2S-000008`, `-000013`) | No default or native VLAN on host ports | Host ports native in user VLANs (`port1`, `port2` since Chapter 04) | |
    | `CISC-L2-000250` (`SRG-NET-000512-L2S-000011`) | Host ports as access ports | `discard-mode all-tagged` (Lab 8.5 step 11) | |

    Block intra-VLAN traffic itself maps to `SRG-NET-000715-L2S-000120` in
    [Volume CLXXII, Chapter 11](../../volume-172-disa-srgs-and-stigs/chapters/11-fortiswitch-feature-version-and-srg-map.md).
    Lab 12.5 applies the hardening set; this table is its rehearsal.

**Track 2:** Run steps 2, 4 (with `10.174.41.100` in place of `<LEASE_A>`), 6,
and 7's controller blocks on your controller (on FGT-1 alone, P3 is free unless
Lab 4.1 used it), and step 8's `show`.
Check them with `show system interface fsw-users`, `show system proxy-arp`, and
`show firewall policy <P3_ID>`. If Lab 2.2's third outcome applies, also run
steps 10 and 11's managed-switch blocks against `S248EPTF18000000`. Do Parts C
and D as written; skip the endpoint and switch steps.

**Track 2: read-and-predict.**

1. Two hosts in an access VLAN, with proxy ARP for both, `allow-traffic-redirect
   disable`, and no policy between them. Predict the ping and what `ip neigh`
   shows on the first host. **Answer:** the neighbor entry shows the FortiGate's
   MAC address (proxy ARP answered), and the ping fails at the FortiGate for
   lack of a policy.
2. A FortiLink interface is a member of a software switch, and an administrator
   enables `switch-controller-access-vlan` on a VLAN. Predict the effect.
   **Answer:** none; intra-VLAN blocking is not supported when the FortiLink
   interface type is a hardware or software switch (p. 262).
3. Predict whether an FS-124F can block intra-VLAN traffic on 20 VLANs.
   **Answer:** no; note 7 limits the FS-108F and FS-124F to 16 access VLANs, and
   the auto-created quarantine VLAN already counts as one.

**Expected result:** Track 1: with intra-VLAN blocking, endpoint A reached its
gateway but not endpoint B; proxy ARP made the FortiGate the next hop; the
result with the redirect at its recorded value is recorded; with the redirect
disabled the ping failed until P3 allowed it, and the sniffer showed both legs;
`access-vlan-mode` is `legacy`; `port4` is down and labeled; `port1` discards
tagged frames and still works; the private VLAN predictions and the Part D
evidence column are filled in. Track 2: the controller objects were built and
the predictions are answered.

**Negative test:** Disable P3 and repeat the ping from endpoint A to
`10.174.41.20`:

```text
FGT # config firewall policy
edit <P3_ID>
set status disable
next
end
```

Predict and observe: the ping fails again, and endpoint A's neighbor entry
still shows the FortiGate's MAC address: the switch keeps the hosts apart, and
without a policy the FortiGate drops the traffic. Track 2: prediction 1 is the
negative test.

**Rollback:** Remove the policy and its object first, then the proxy ARP entry,
then restore the global setting to the value you recorded in step 2 (shown
here as the 7.6.0 default, `enable`), the VLAN, and the ports:

```text
FGT # config firewall policy
delete <P3_ID>
end
FGT # config firewall address
delete "fsw-users-net-174"
end
FGT # config system proxy-arp
delete 1
delete 2
end
FGT # config system global
set allow-traffic-redirect enable
end
FGT # config system interface
edit "fsw-users"
set switch-controller-access-vlan disable
next
end
FGT # config switch-controller managed-switch
edit <SWITCH_SN>
config ports
edit "port1"
set discard-mode none
next
edit "port2"
set vlan "fsw-iot"
next
edit "port4"
unset description
set status up
next
end
next
end
```

```bash
# endpoint B
sudo ip addr del 10.174.41.20/24 dev <IFACE_B>
ping -c 3 10.174.43.1
```

Confirm that endpoint A reaches `10.174.41.1`, that `show firewall policy`
lists only P1 and P2 (on C2, P3 is free again), and that `show
switch-controller managed-switch <SWITCH_SN>` shows `port1` and `port2` as
Chapter 07 left them. Restore `fgt-pre-8-1-174.conf` only if something else
differs.

**Lab verified by:** *pending*

## Lab Verification

Complete this sign-off once Labs 8.1 to 8.5 have been run end to end, including
each negative test. Until then, the labs are unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

DHCP snooping is enabled per VLAN on the FortiGate and trusts only the ports
set as trusted, so a rogue server on an access port is ignored; with the default
`drop-untrusted`, it never even sees a client's request. The binding database
it builds feeds dynamic ARP inspection, which drops ARP packets that do not
match a binding, and IP source guard, which drops IPv4 traffic from unbound
source addresses on the 200 Series; statically addressed hosts need static
entries for both. Option 82 tells the server where a request came from, and the
allowed server list limits who may answer. Storm control caps broadcast,
unknown unicast, and unknown multicast globally, per switch, or per port, and a
rate of 0 drops ARP and DHCP too. In FortiLink mode only ingress ACLs exist,
only on models outside note 16, as policies grouped and bound to ports.
Intra-VLAN blocking turns the FortiGate into the only path between hosts, which
proxy ARP, `allow-traffic-redirect disable`, and a policy then control; private
VLANs are the standalone counterpart. The chapter ends with every setting
removed and the C2 slot P3 free.

- [ ] I saw a rogue DHCP server answer without snooping and stay silent with
      it, and I know whether my FortiLink trunk is DHCP-trusted.
- [ ] I read endpoint A's binding from the controller and the switch, and
      recorded the option 82 mapping and its effect on the lease.
- [ ] A spoofed ARP packet was dropped and counted with DAI on, and endpoint B
      worked only after its static entry.
- [ ] I know whether my switch supports IP source guard, and on S3 I saw an
      unbound source address dropped.
- [ ] A storm-control policy cut a broadcast flood to about its rate, and I saw
      that a rate of 0 also stops ARP.
- [ ] On S3, an ingress ACL counted and dropped traffic on the port where it
      entered; on S1 or S2, I recorded FortiOS's response and know Lab 11.4
      covers ACLs.
- [ ] Intra-VLAN blocking separated endpoints A and B, and P3 let them ping
      through the FortiGate.
- [ ] `port4` was shut and labeled, `port1` discarded tagged frames, and I can
      predict private VLAN reachability.
- [ ] Every setting from Labs 8.1 to 8.5 is removed, `allow-traffic-redirect` is
      back at its recorded value, and on C2 P3 is free.
