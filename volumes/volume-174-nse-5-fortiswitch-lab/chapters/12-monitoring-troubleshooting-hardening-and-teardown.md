# Chapter 12: Monitoring, Troubleshooting, Hardening, and Teardown

## Learning Objectives

- Read a managed switch's MAC table, LLDP neighbors, port statistics, cable
  test, and topology from both the controller and the switch, and say which
  view each command gives.
- Export switch telemetry to the collector on `ubuntu-ws`: SNMPv3 queries and
  SNMP traps, sFlow samples, and flow records (NetFlow or IPFIX), within the C2
  policy budget.
- Capture traffic four ways: the FortiGate sniffer on the FortiLink and VLAN
  interfaces, an on-switch packet capture, a FortiSwitch port mirror (SPAN), and
  RSPAN to the controller, and know which switch options support each.
- Induce the common FortiLink faults (link down, LLDP filtered, neighbor
  detection changed, switch deauthorized, inter-switch link member lost),
  record each fault's signature, and predict the signatures of the faults you
  do not induce (wrong VDOM, incompatible firmware).
- Harden the managed switch against the Volume CLXXII FortiSwitch
  prerequisites (remote logging, NTP, SNMPv3, management access, DHCP snooping
  and VLAN hygiene, flow collection, image integrity) and collect evidence for
  each row, including the rows FortiLink mode cannot meet.
- Tear the lab down: retire every switch, return every controller to its
  pre-volume configuration, undo the Proxmox, Nexus, and VM changes of
  Chapter 02, and confirm the result with a final checklist.

## Theory and Architecture

### What this chapter does

Chapters 02–11 built and exercised the lab. This chapter watches it, breaks
it on purpose, hardens it, and then removes it. It covers the exam's fourth
domain (monitoring and troubleshooting) and ends the volume.

| Lab | Exam task | Builds or proves | Track 1 | Track 2 |
| --- | --- | --- | --- | --- |
| 12.1 | 4.3 (and 1.4 supporting) | Information views: MAC table, LLDP, port statistics, cable test, topology | Hands-on | Read-and-predict |
| 12.2 | 4.3 | SNMP, sFlow, and flow export to `ubuntu-ws` | Hands-on (sFlow and flow export not on S1) | Build + predict |
| 12.3 | 4.1 | FortiGate sniffer, on-switch capture, SPAN, RSPAN | Hands-on (on-switch capture not on S1; RSPAN S3 only) | FortiGate sniffer live + predict |
| 12.4 | 4.2 | FortiLink fault clinic | Hands-on (two faults predict only) | Read-and-predict |
| 12.5 | Hardening (Volume CLXXII) | Remote log, NTP, SNMPv3, access, snooping, hygiene, evidence | Hands-on | Build (controller side only) |
| 12.6 | Teardown | Switches retired, controllers restored, Proxmox, Nexus, and VMs returned | Hands-on | Hands-on (controller and hypervisor) |

### Two views of one switch

A managed switch can be read from the controller, which asks the switch over
the FortiLink management session, or from the switch's own CLI (console or
SSH). The controller's view needs a working session; the switch's view still
works when FortiLink is down, which is why the fault clinic uses both.

| Question | Controller (`FGT #`) | Switch (`FSW #`) | Source |
| --- | --- | --- | --- |
| Is the switch managed, and on which build? | `execute switch-controller get-conn-status` | `execute switch-controller get-conn-status`, `get system status` | FortiLink Guide 7.6.7, p. 52; FortiSwitchOS 7.6.7 CLI Reference, pp. 451, 535 |
| How are the switches cabled to the controller and to each other? | `execute switch-controller get-physical-conn standard <FL_PORT>`; GUI topology views | `get switch lldp neighbors-summary`, `diagnose switch trunk summary` | FortiLink Guide, pp. 181, 319, 322–324; CLI Reference, pp. 381, 499 |
| Which MAC addresses are where? | `diagnose switch-controller switch-info mac-table <switch>` (FortiOS 8.0.1 reference only); `diagnose switch-controller mac-cache show <switch>` | `diagnose switch mac-address list` | FortiOS 8.0.1 CLI Reference; FortiLink Guide, p. 334; CLI Reference, p. 354 |
| Which LLDP neighbors does a port see? | `diagnose switch-controller switch-info lldp neighbors-summary <switch>` (also `neighbors-detail`, `stats`) | `get switch lldp neighbors-summary` | FortiLink Guide, p. 176; CLI Reference, p. 499 |
| How busy or how faulty is a port? | `diagnose switch-controller switch-info port-stats <switch> <port>`; `trigger reset-hardware-counters` and `restore-hardware-counters` | `diagnose switch physical-ports port-stats`, `summary` | FortiLink Guide, pp. 336–339; CLI Reference, pp. 369, 375 |
| Is the cable good? | `execute switch-controller switch-action cable-diag <switch> <port>` (FortiOS 8.0.1 reference); GUI **Cable Test** | `diagnose switch physical-ports cable-diag <port>` | FortiLink Guide, pp. 331–332; CLI Reference, p. 363 |
| What is the switch's hardware and fan state? | `diagnose switch-controller switch-info status` and `fan` (**FortiOS 7.6.3 and later**) | `get system status` | FortiLink Guide, pp. 332–333 |

The FortiOS 7.6.0 CLI Reference holds configuration commands only, so every
`execute` and `diagnose` command above is matched against the FortiLink Guide
7.6.7 or, where the guide prints no syntax line, against the FortiOS 8.0.1 CLI
Reference as a cross-check. A command that only the 8.0.1 reference lists may
take different arguments on FortiOS 7.6.2; type `?` after it on your build.
FGT-1 runs FortiOS 7.6.2, so `switch-info status` and `switch-info fan` are
**read-only** in this chapter on C2 and on any controller below 7.6.3.

The GUI has three views the CLI does not reproduce: **WiFi & Switch
Controller > Managed FortiSwitches** with the **Topology** view (green when the
FortiLink is up; a dashed line and a broken-link icon when it is down),
**WiFi & Switch Controller > FortiSwitch Ports** (faceplates, per-port VLANs,
PoE, DHCP snooping, transceivers, and **View Statistics**), and the
**Diagnostics and Tools** pane of each switch (health, cable test, LED blink,
logs, clients). **Security Fabric > Physical Topology** shows the same switches
in the fabric (FortiLink Guide 7.6.7, pp. 322–335).

### Telemetry the switch can export

| Export | Controller object | Transport and default port | What the documentation says |
| --- | --- | --- | --- |
| Switch logs to the FortiGate | `config switch-controller switch-log` | Over FortiLink | Enabled by default; the FortiGate tags entries with user `fortiswitch-syslog` (FortiLink Guide 7.6.7, p. 291) |
| Switch logs to syslog | `config switch-controller remote-log` (`syslogd`, `syslogd2`) | UDP 514 | Disabled by default; one or two servers, severity, facility, CSV (p. 292) |
| SNMP queries | `snmp-sysinfo`, `snmp-community`, `snmp-user` under `config switch-controller` | UDP 161 to the switch | Read-only; needs a firewall policy **toward** the FortiLink interface and `snmp` in the switch's internal-interface access (pp. 302–304) |
| SNMP traps | `snmp-community` hosts | UDP 162 from the switch | Needs a firewall policy **from** the FortiLink interface; at most eight trap hosts per switch (p. 302) |
| sFlow | `config switch-controller sflow`, plus `packet-sampler` per port | UDP 6343 | sFlow version 5; CPU intensive, so avoid high sampling rates for long periods; needs a policy from the switch to the collector (pp. 308–309) |
| Flow export | `config switch-controller flow-tracking` with `config collectors` | Collector port you choose (UDP, TCP, or SCTP) | NetFlow 1, 5, 9, or IPFIX; sample modes `local`, `perimeter`, `device-ingress` (pp. 309–312) |

Two details shape the lab. First, the controller's policies decide what
reaches the collector: Chapter 02's P2 already allows UDP 514, 162, and 6343
from the FortiLink interface to `ubuntu-ws`, but an SNMP **query** goes the
other way and needs a policy of its own, which on C2 is the last free slot,
P3. Second, the guide and the reference describe flow tracking differently.
The FortiOS 7.6.0 CLI Reference gives the defaults `sample-mode perimeter`,
`format netflow9`, and `level ip`, and describes perimeter mode as sampling
"all switch fabric ports and fortilink port at the ingress"; the FortiLink
Guide (p. 311) says perimeter mode samples all ports that receive data traffic
**except** ISL and ICL ports. Lab 12.2 records which ports export flows.

The FortiOS SNMP OIDs for managed switches (`fgSwCpu`, `fgSwMemory`,
`fgSwPortStatus`, FortiLink Guide, p. 307) are read from the FortiGate's own
SNMP agent, not the switch's; this volume does not configure the FortiGate's
agent, so it uses them only in a prediction.

### Ways to capture packets

| Method | Where it runs | Controller object or command | Switch support (feature matrix 7.6.7) |
| --- | --- | --- | --- |
| FortiGate sniffer | The controller's FortiLink port and its VLAN interfaces | `diagnose sniffer packet <interface> '<filter>' <verbose> <count> <tsformat>` | Not a switch feature; every option, Track 2 included |
| On-switch packet capture | The switch, one switch or system interface per profile | Switch CLI: `config system sniffer-profile`, `execute system sniffer-profile` | Chain in the 1xxE/1xxF column for the FS-124F, FS-148E, and FS-148F only; chain in the 200 Series |
| Port mirror (SPAN) | One switch, source ports to a local destination port | `config mirror` under the managed-switch entry | Chain in both columns |
| RSPAN | Mirrored frames sent in VLAN 4092 to the controller's `rspan` interface | `config switch-controller traffic-sniffer`, `set mode rspan` | Dash in 1xxE/1xxF; chain in the 200 Series |
| ERSPAN | Mirrored frames in GRE to a collector IP address | `traffic-sniffer`, `set mode erspan-auto`, `set erspan-ip` | Dash in 1xxE/1xxF; chain in the 200 Series |
| FortiOS one-arm sniffer | The `rspan` VLAN interface as an IDS input (FortiOS 7.4.1 and FortiSwitchOS 7.4.1 or later) | `ips-sniffer-mode enable` and `config firewall sniffer` | Dash in 1xxE/1xxF; chain in the 200 Series |

The FortiLink Guide 7.6.7 documents no controller command that starts an
on-switch capture; the FortiOS 8.0.1 CLI Reference lists a `diagnose
switch-controller traffic-capture` group, which this volume treats as an 8.0
feature and does not use. Lab 12.3 therefore creates the capture profile on the
switch console. The guide also warns that changes made directly on a managed
switch are unknown to the FortiGate and are lost after the switch restarts
(p. 14), so the lab removes the profile as soon as it has read the capture.
The Administration Guide gives the profile limits: eight profiles and a 20 MB
RAM disk on the FS-124F, FS-148E, and FS-148F, eight and 50 MB on the 2xx
models, and every `.pcap` file is deleted when the switch is power cycled
(FortiSwitchOS 7.6.7 Administration Guide, pp. 133–136).

When RSPAN or ERSPAN is used, the switch controller adds a traffic policy named
`sniffer` (a policer) to limit the mirrored traffic; the feature matrix lists
the traffic policer only for the 200 Series and larger models in this volume's
columns (FortiLink Guide, p. 293). ERSPAN cannot be combined with SPAN or
RSPAN, and its collector must answer ICMP ping from the switch (p. 293).

### FortiLink fault signatures

The FortiLink Guide 7.6.7 has no troubleshooting chapter. What it gives is the
output shape of the tools and a few statements: a link shown dashed with a
broken-link icon can be down because of the cable or because the switch's
firmware is out of step with the FortiGate's, and the firmware must be
compatible (p. 323). The fault clinic therefore builds its signatures from
those shapes and from what you record.

| Fault | Where it shows first | Documented shape | Undocumented, so recorded in Lab 12.4 |
| --- | --- | --- | --- |
| FortiLink cable unplugged | `get-conn-status` on the controller | `Authorized/Down`, ADDRESS `0.0.0.0` (the guide's upgrade example, p. 348); topology line dashed (p. 323) | How long the controller takes to notice, and how long the switch takes to return |
| LLDP filtered between controller and switch | `switch-info lldp neighbors-summary` | Discovery needs LLDP when `fortilink-neighbor-detect lldp` is set (Chapter 02) | Whether an already authorized session survives without LLDP |
| Neighbor detection changed on the FortiLink interface | `get-conn-status`, LLDP views | Two methods, `fortilink` and `lldp` (FortiLink Guide, p. 24) | Whether a managed switch notices the change at all |
| Switch not authorized (deauthorized) | `get-conn-status` STATUS | `Discovered/Down`, VERSION and ADDRESS `N/A` for a never-authorized switch (p. 52) | The STATUS of a switch that was authorized and then deauthorized, and whether it resets (see `switch-on-deauth`) |
| Switch managed in another VDOM | `get-conn-status` header | The table is per VDOM: `Managed-devices in current vdom vdom1:` (p. 52) | — (predicted only) |
| Incompatible firmware | `get-conn-status` VERSION and STATUS; topology | Firmware must be compatible (p. 323); check the FortiLink Compatibility table (p. 12) | — (predicted only; the lab never downgrades) |
| Configuration sync failed | `get-conn-status` FLAG | FLAG `E` (p. 52); `get-sync-status all`, `trigger config-sync` (pp. 318–319, 343) | The fields of an in-sync row (Lab 3.4 recorded them) |
| ISL or ICL member lost (S3) | `switch-info mclag icl`; switch `diagnose switch mclag icl` and `trunk summary` | ICL redundancy needs at least two links (FortiLink Guide, p. 89) | What the controller reports while one member is down |

On the switch side, `diagnose switch fortilink-auth status <port>` and
`statistics <port>` report FortiLink secure-fabric authentication per port
(CLI Reference, p. 352; FortiLink Guide, pp. 181–182). The secure fabric
authenticates and encrypts ISLs only; the link between the FortiGate and a
switch is always unencrypted (p. 179). This volume never enables it, so on its
ports the command shows the default (legacy, no authentication); the lab reads
it once as a baseline.

### Hardening a switch that a FortiGate manages

In FortiLink mode the controller owns the switch's configuration, so hardening
is done with controller objects. Some controls are not available at all,
because the feature matrix marks them standalone only (a check mark):

| Control | In FortiLink mode | Feature matrix 7.6.7, 1xxE/1xxF and 200 Series |
| --- | --- | --- |
| Admin password and console login | `switch-profile` (`login-passwd-override`, `login-passwd`, `login`), bound per switch (FortiLink Guide, pp. 43–44) | Not a matrix row |
| Per-interface admin access | `config switch-controller security-policy local-access` (`mgmt-allowaccess`, `internal-allowaccess`), bound with `access-profile` (p. 45) | Not a matrix row |
| Remote admin authentication (RADIUS, TACACS+) | Not available | Check (standalone only) in both columns |
| Syslog | `remote-log` (UDP); `switch-log` to the FortiGate | Syslog collection chain in both; reliable (TCP) syslog check only |
| NTP | The FortiGate serves NTP on the FortiLink interface (`config system ntp`, `server-mode`, `interface`; FortiLink Guide, p. 25) and in the FortiLink DHCP server (`ntp-service local`, p. 37) | NTP **server** on the switch: check only |
| SNMPv3 | `switch-controller snmp-user` with `auth-priv` | Support for switch SNMP OID chain in both |
| Management VLAN | The FortiLink management VLAN, 4094 by default (`switch-controller-mgmt-vlan`, p. 34) | Not a matrix row |
| DHCP snooping, DAI, storm control, unused ports | Chapter 08's controller objects | Chain in both (IP source guard 200 Series only) |
| Flow collection | `sflow`, `flow-tracking` | sFlow and flow export as in the telemetry table |
| Image integrity | Switch `get system status` (`Firmware Signature`), `diagnose sys firmware info`, `execute verify image` | OS image signature verification chain in both, except the FS-224D-FPOE and FS-248D (note 17); the "CLI command reports if BIOS and firmware signatures are valid" row is a check in both, with the same two 200 Series models excluded |

[Volume CLXXII, Chapter 11](../../volume-172-disa-srgs-and-stigs/chapters/11-fortiswitch-feature-version-and-srg-map.md)
wrote its prerequisites P1–P18 for standalone FortiSwitchOS 8.0.0 and FortiOS
8.0.1. Lab 12.5 maps each row this chapter can meet to its FortiLink-mode
equivalent, re-checked against the 7.6 references, and records the rows it
cannot meet as exceptions. Lab 8.5 Part D was its rehearsal for the Layer 2
rows.

### Firmware and image management, revisited

Chapter 03 pushed firmware from the controller; this chapter cleans up after
it and checks integrity.

- **On the controller**, `execute switch-controller switch-software
  list-available` lists the uploaded images (FortiLink Guide, p. 346).
  Removing one is `execute switch-controller switch-software delete
  <all>|<image-name>` in the FortiOS 8.0.1 CLI Reference; the FortiLink Guide
  7.6.7 prints no delete command, so type `?` after `switch-software` on your
  build first.
- **On the switch**, `diagnose sys flash list` shows the flash partitions, the
  image in each, and which partition boots next (CLI Reference, p. 389).
  `execute verify image {primary | secondary}` checks the stored image ("No
  issue found!" in the reference's example, p. 464), and `diagnose sys firmware
  info` reports whether the BIOS and firmware signatures are valid (p. 389).
  From FortiSwitchOS 7.4.0 the GUI warns about an unverified image as well
  (Administration Guide, p. 60).
- **Before every upgrade**, the switch profile's `revision-backup-on-upgrade`
  (bound since Lab 3.4) saves a configuration revision on the switch;
  `revision-backup-on-logout` does the same at every logout (FortiLink Guide,
  p. 352).

### Retiring switches and returning the controller

The FortiLink Guide (p. 322) gives two ways to release a managed switch, both
of which reset it to factory defaults: `execute switch-controller factory-reset
<switch-id>` (the switch may be discovered and authorized again) and `execute
switch-controller switch-action set-standalone <switch-id>` (the controller
does not detect and authorize it again automatically). Lab 3.5 and Chapter 11
used the second; the teardown uses it again, then deletes the entries. The
guide's `switch-on-deauth {factory-reset | no-op}` option (p. 43) would reset
or keep a switch's password on deauthorization, but it is not in the FortiOS
7.6.0 CLI Reference, so the lab only checks for it with `?`. Deauthorizing
from **Security Fabric > Fabric Connectors** also adds the serial to the
`show system csf` trusted list with `action deny` (p. 321); the teardown checks
that list.

The controllers return to the configurations saved before the volume touched
them. Chapter 02 saved three such files on VM 140, one per option:
`c1-fgt-base-174.conf` (C1, after the factory reset and lab addressing),
`fgt1-pre-174.conf` (C2, before `port3` left VLAN 202), and
`fgt-c3-pre-174.conf` (C3, before `port4` was added). Lab 12.6 removes the lab
objects by hand, compares the result with that file, and falls back to
restoring the file if anything is left. If FortiLink refuses to let go of its
interface, the guide's advice is to disable it first (`set fortilink disable`,
p. 33; the guide prints the block under `config switch interface`, which is a
misprint for the FortiOS `config system interface` that Chapter 02 used).

### Where the sources differ

| Topic | One source | Another source | This chapter |
| --- | --- | --- | --- |
| sFlow collector lines | FortiLink Guide prints `collector-ip <x.x.x.x>` without `set` (p. 308) | FortiOS 7.6.0 CLI Reference: `set collector-ip`, `set collector-port` | Uses `set` |
| Flow tracking perimeter mode | Guide: all data ports except ISL and ICL (p. 311) | 7.6.0 reference: switch fabric ports and the FortiLink port at ingress | Records which ports export |
| `remote-log` entry names | Guide: `edit {syslogd \| syslogd2}` (p. 292) | 7.6.0 reference: `edit <name>` (up to 35 characters) | Uses `syslogd`, valid in both |
| Disabling FortiLink | Guide: under `config switch interface` (p. 33) | FortiOS has no such table; `fortilink` is a `config system interface` option | Uses `config system interface` |
| `switch-on-deauth` | Guide documents it (p. 43) | Not in the 7.6.0 CLI Reference | Checks with `?` only |
| Status and fan commands | Guide: FortiOS 7.6.3 and later (p. 332) | FortiOS 8.0.1 reference lists them | Read-only on FGT-1 7.6.2 |
| Image delete on the controller | Not in the FortiLink Guide 7.6.7 | FortiOS 8.0.1: `switch-software delete <all>\|<image-name>` | Check with `?` first |
| Vol CLXXII image check | Vol CLXXII Ch 11 (8.0.0): `diagnose sys firmware info` | FortiSwitchOS 7.6.7 CLI Reference: the same command (p. 389) | Uses it, plus `execute verify image` |

### Model support for this chapter

From the FortiSwitchOS 7.6.7 feature matrix (`temp/nse5fsw/fm767.txt`, the
position-based read); chain = standalone and managed, check = standalone only,
dash = not supported:

| Feature | 1xxE/1xxF (S1 FS-108F, S2 FS-124F) | 200 Series (S3) | Labs |
| --- | --- | --- | --- |
| Port statistics CLI ("Add CLI to show the details of port statistics") | Chain | Chain | 12.1 |
| TDR (cable diagnostics) | Chain | Chain | 12.1 |
| Support for switch SNMP OID | Chain | Chain | 12.2 |
| MAC notification SNMP trap | Chain | Chain | 12.2 (optional) |
| sFlow (IPv4) | Chain, models (124F, 148E, 148F) | Chain | 12.2 |
| Flow export (IPv4) | Chain, models (124F, 148F) | Chain | 12.2 |
| FortiView Internal Hubs | Dash | Chain | 12.2 (described only) |
| Packet capture | Chain, models (124F, 148E, 148F) | Chain | 12.3 |
| SPAN | Chain | Chain | 12.3 |
| RSPAN and ERSPAN (IPv4) | Dash | Chain | 12.3 |
| FortiOS one-arm sniffer | Dash | Chain | 12.3 (described only) |
| Traffic policy (policer) | Dash | Chain | 12.3 (RSPAN) |
| Syslog collection | Chain | Chain | 12.5 |
| Reliable syslog | Check | Check | 12.5 (exception) |
| RADIUS and TACACS+ for administrative authentication | Check | Check | 12.5 (exception) |
| NTP server (on the switch) | Check | Check | 12.5 (not used) |
| FortiLink Secure Fabric (first row) | Chain | Chain | 12.4 (baseline read) |
| OS image signature verification | Chain | Chain, except FS-224D-FPOE and FS-248D (note 17) | 12.5 |

The FS-108F is the only switch option without sFlow, flow export, and on-switch
packet capture; on S1 those steps are read-and-predict. The FS-124F lacks RSPAN
and ERSPAN, so on S1 and S2 the RSPAN step is read-and-predict.

## Design Considerations

### Exam tasks this chapter practices

| Exam task | Labs here | Track 2 mode |
| --- | --- | --- |
| 4.1 Packet capture | 12.3 (primary) | FortiGate sniffer live on `port2`; switch captures predicted |
| 4.2 FortiLink troubleshooting | 12.4 (primary) | Predict every signature |
| 4.3 View and extract information | 12.1, 12.2 (primary) | Build the export objects; predict the rest |
| 1.4 Switching and routing | 12.1 (supporting, MAC table) | Predict |

### The controller and the C2 budget

| Item | Change in this chapter | Removed |
| --- | --- | --- |
| P1, P2 | Unchanged; P2 carries syslog (514), traps (162), sFlow (6343), and, after Lab 12.2, flow export (2055) | Lab 12.6 |
| `lab-svc-174` | Gains UDP 2055 for flow export in Lab 12.2 | Lab 12.6 (the object is deleted) |
| P3 | `P3-snmp-174`, `ubuntu-ws` to the FortiLink port, service `SNMP`, from Lab 12.2 to Lab 12.6 (C1: with source NAT) | Lab 12.6 |
| Routes and interfaces | None added | — |

On C2 that uses all three policy slots from Lab 12.2 onwards. No other lab in
this chapter needs a policy: the fault clinic, the captures, and the hardening
use only existing paths. If your C2 P1 does not exist, P3 is still the only
policy this chapter adds.

### Names, backups, and placeholders

| Item | Value | Lab |
| --- | --- | --- |
| Controller backups on VM 140 | `fgt-pre-12-2-174.conf`, `fgt-pre-12-4-174.conf`, `fgt-pre-12-5-174.conf`, `fgt-final-174.conf` (before teardown), `fgt-teardown-174.conf` (after teardown) | 12.2, 12.4, 12.5, 12.6 |
| Console capture | `fsw-final-174.txt` (the switch's last managed configuration) on the console host | 12.6 |
| SNMP | sysinfo enabled; SNMPv3 user `snmp-174` (`auth-priv`, `sha256`, `aes128`); v2c trap community `trap-174` (removed in Lab 12.5) | 12.2, 12.5 |
| Local-access policy | `la-174`: `mgmt-allowaccess https ping ssh`, `internal-allowaccess https ping ssh snmp` | 12.2 |
| Flow collectors | sFlow `10.200.0.20:6343`; flow tracking collector `ws-174` `10.200.0.20:2055` UDP | 12.2 |
| Captures and mirrors | Switch profile `cap-174`; mirror `mir-174` (`port1` to `port2`); RSPAN target `port1` (S3) | 12.3 |
| Hardening objects | `remote-log` `syslogd`; storm-control policy `storm-uu-174`; `port4` description `unused-174` | 12.5 |
| New placeholders | `<SNMP_AUTH_PASSWORD>`, `<SNMP_PRIV_PASSWORD>` (SNMPv3 secrets, at least eight characters); `<WS_IFACE>` (the wired interface of `ubuntu-ws`); `<FL_DHCP_ID>` (the DHCP server on the FortiLink port); `<USERS_DHCP_ID>` (the DHCP server on `fsw-users`) | 12.2, 12.5, 12.6 |

`<SWITCH_SN>`, `<FSWB_SN>`, `<FSW_FL_PORT>`, `<FL_TRUNK>`, `<P1_ID>`,
`<P2_ID>`, `<P3_ID>`, `<LEASE_A>`, `<IFACE>`, `<IFACE_B>`, `<MODEL>`,
`<PORT3_MAC>`, `<PORT4_MAC>`, `<NEW_NIC>`, `<PCI_ADDR>`, and `<TEST202_IP>`
keep their meanings from earlier chapters. `10.255.1.2` stands for the
switch's FortiLink address; if Lab 11.5 recorded a different one, use that.

### The teardown order

Retirement must happen while the controller still manages the switch, and in
an order that never strands a switch:

1. **Archive** the controller's last configuration and the switch's last
   managed configuration.
2. **Retire the switches from the controller.** On S3, retire `FSW-B` first: it
   reaches the controller only through `FSW-A` (Chapter 06), so it would lose
   its path if `FSW-A` were reset first.
3. **Remove the controller's lab objects** in dependency order (policies before
   the objects they name, zone before its member interfaces, VLAN interfaces
   before their parent's FortiLink setting), compare the result with the
   pre-volume file, and restore that file if anything is left.
4. **Return the hypervisor** (C2, C3): the FortiLink vNIC or passed-through NIC,
   the `vmbrFL` bridge, the passthrough modules, and the helper script.
5. **Return the network**: the Nexus access ports used in Chapter 02 (and on C1
   the controller's two ports).
6. **Return the services and hosts**: `radius-174` (VM 174), the collectors and
   listener on `ubuntu-ws`, the endpoints, the console host, and the files on
   VM 140.
7. **Check** everything against the final checklist.

### Manual removal or restore

| | Manual removal, then compare (primary) | Restore the pre-volume file (fallback) |
| --- | --- | --- |
| Keeps unrelated changes made since Chapter 02 | Yes | No: everything since the backup is lost |
| Proves you know every object the volume created | Yes | No |
| Reboots the controller | No | Yes |
| Leaves nothing behind | Only if the comparison is clean | Yes |
| Use when | The controller is a shared lab device (FGT-1) | The comparison shows leftovers you cannot remove, or the controller exists only for this lab |

On C2, the restore also brings back the VLAN 202 policies and DHCP server that
Lab 2.1 deleted; on the manual path you re-create them from the `show` output
Lab 2.1 recorded. The hypervisor and the network must be returned on both
paths.

### Everything the volume created

| Object | Where | Created in | Still there at the start of this chapter |
| --- | --- | --- | --- |
| FortiLink interface (`port3`, `port4`, or `<FL_PORT>`, alias `fortilink`, `10.255.1.1/24`) and its DHCP server | Controller | Lab 2.2 | Yes |
| Auto-created VLAN interfaces (quarantine, rspan, voice, video, onboarding, nac segment) and their DHCP servers | Controller | Lab 2.4 (first discovery, from the templates) | Yes |
| `radius-174` server, `lab-svc-174`, addresses `radius-174` and `ubuntu-ws`, policy `P2-fortilink-services` | Controller | Lab 2.5 | Yes |
| Managed-switch entries `<SWITCH_SN>` (and `<FSWB_SN>` on S3; `S248EPTF18000000` on Track 2) | Controller | Labs 3.1, 6.2, 2.2/3.1 | Yes |
| Switch profile `fsw-174-prof` | Controller | Lab 3.4 | Yes |
| Uploaded switch images | Controller | Lab 3.3 | Possibly |
| VLAN interfaces `fsw-users`, `fsw-voice`, `fsw-iot`, `fsw-guest`, `fsw-tenant`; DHCP server on `fsw-users`; zone `FSW-LAN`; `FSW-LAN` in P1 and P2; `fsw-lan-174` (if P1 needed it); C1 `P1-fsw-lan-internet` | Controller | Lab 4.1 | Yes (unless C2's Lab 4.1 was NO-GO) |
| STP settings `lab-174` revision 1, `stp-instance` 1 | Controller | Lab 5.1 | Yes |
| User group `dot1x-174`, security policies `dot1x-174-port` and `mab-174` | Controller | Lab 7.1, 7.2, 7.3 | Yes |
| C1: hostname `c1-fgt`, WAN and services addresses, default route, `<FL_PORT>` out of the hardware switch | C1 controller | Lab 2.1 | Yes |
| C2: `port3` out of VLAN 202 (policies and DHCP server deleted), `net2` moved to `vmbrFL` or replaced by `hostpci0` | FGT-1, proxmox-1 | Labs 2.1, 2.3 | Yes |
| C3: `net3` (`port4`) on `vmbrFL`, or `hostpci0` | proxmox-1 | Labs 2.1, 2.3 | Yes |
| `vmbrFL` and `<NEW_NIC>` stanzas, `/root/fl-path-check.sh`, `tcpdump` (if installed), `/etc/modules-load.d/vfio.conf` (Option B) | proxmox-1 | Labs 2.3, Implementation and Automation of Chapter 02 | Yes |
| VM 174 `radius-174` (FreeRADIUS, clients, users, PEAP certificates, `authorize.pre-7-3`) | proxmox-1 | Labs 2.5, 7.1–7.3 | Yes |
| `/etc/rsyslog.d/10-fsw-174.conf` | `ubuntu-ws` | Lab 2.5 | Yes |
| `wpasupplicant`, `/etc/wpa_supplicant/wired-174.conf`, `tcpdump`, `iputils-arping` | Endpoint A | Labs 2.5, 7.2, 8.1 | Yes |
| `dnsmasq` (disabled), static `10.174.43.20/24`, `tcpdump`, `iperf` | Endpoint B | Labs 2.5, 4.2, 8.1, 10.2 | Yes |
| Nexus `Eth1/<free>` (VLAN 99, edge), shut | Nexus | Lab 2.4, Chapter 11 | Yes (shut) |
| C1 Nexus ports for `<WAN_PORT>` (VLAN 99) and `<SVC_PORT>` (VLAN 200) | Nexus | Lab 2.1 | Yes (C1 only) |
| Backups, console captures, and images | VM 140, console host | Every chapter | Yes |
| This chapter's objects (see the names table) | Controller, `ubuntu-ws` | Labs 12.2–12.5 | Created here |

Lab 12.6 removes each row and the final checklist ticks it off.

## Implementation and Automation

The labs are the implementation. Three habits keep this chapter's evidence
useful.

**Watch the collector in one place.** Save this read-only script on
`ubuntu-ws` as `~/watch-174.sh` (replace `<WS_IFACE>`). It prints the first
packets of each export the switch sends, so one command shows whether syslog,
traps, sFlow, and flow export arrive. It needs `tcpdump` (`tcpdump(8)`):

```bash
#!/bin/sh
# Read-only: show what the managed switch (10.255.1.2) sends to ubuntu-ws.
IF=<WS_IFACE>
SW=10.255.1.2
for p in 514 162 6343 2055; do
  echo "== UDP $p from $SW (up to 3 packets, 40 s) =="
  sudo timeout 40 tcpdump -n -i "$IF" -c 3 "udp port $p and src host $SW"
done
```

**Save the switch's own view before you change anything.** As in Chapter 11,
log the console to a file with `picocom --logfile` before each lab, so that a
fault you induce leaves a record even if the controller loses the switch.

**Keep an evidence file per hardening row.** Lab 12.5 asks for the output of a
`show` or `diagnose` command for each Volume CLXXII row. Paste each output
under the row's ID in your lab notes, with the date and the controller and
switch builds, the way Volume CLXXII collects evidence.

The FortiOS configuration commands in this chapter were checked against the
FortiOS 7.6.0 CLI Reference with `temp/nse5fsw/verify.py` (`fos76blocks.json`),
and the FortiSwitchOS commands against the FortiSwitchOS 7.6.7 CLI Reference
(`fsw767blocks.json`). FortiOS `execute`, `diagnose`, and non-configuration
`get` commands were matched against the FortiLink Guide 7.6.7 where it prints
them and otherwise against the FortiOS 8.0.1 CLI Reference as a cross-check.
Matched against the FortiLink Guide 7.6.7: `get-conn-status`,
`get-sync-status all`, `switch-action set-standalone`, `switch-software
list-available`, `switch-info lldp`, `port-stats`, `port-properties`,
`mclag icl`, `flow-tracking statistics`, `status`, `fan`, `trigger
reset-hardware-counters` and `restore-hardware-counters`, `mac-cache show`,
and `flow-collector status`. Matched against the FortiOS 8.0.1 CLI Reference
(cross-check): `diagnose sniffer packet`, `switch-info mac-table`,
`switch-info flow-tracking flows`, `get-physical-conn standard`,
`switch-action cable-diag`, `switch-action flow-tracking expire-flows-all`,
`switch-software delete`, `trigger config-sync` with a serial, `diagnose sys
cmdb refcnt`, `diagnose test authserver`, `execute backup config`, `execute
restore config`, and `execute ping`. `get system interface physical` is the
standard FortiOS form used throughout the volume. Matched by hand, because the
verifier cannot parse them: `get switch lldp neighbors-summary` (a syntax line
split over two lines, CLI Reference, p. 499), `diagnose switch physical-ports
summary <port>` and `diagnose switch vlan list <VLAN_ID>` (optional
arguments, pp. 375, 383), `max-pkt-count 20` (the range `<1-maximum>`,
p. 272), and `show system interface internal` and `show` (the `show` forms of
documented tables). `unselect` lines and the `set switch-on-deauth ?` check
are typed at the prompt as the FortiLink Guide prints them (pp. 43, 322). The
Proxmox lines follow `qm(1)` and Chapter 02, the Nexus lines Chapter 02's
NX-OS pattern, and the host commands their manual pages.

## Validation and Troubleshooting

| Symptom | Likely cause | Check |
| --- | --- | --- |
| `snmpwalk` times out | No P3 (C2) or SNMP policy toward the FortiLink port; `snmp` missing from `internal-allowaccess`; wrong user, protocol, or password | `show firewall policy <P3_ID>`; `show switch-controller security-policy local-access la-174`; the switch's `show system interface internal` |
| `snmpwalk` returns an authentication error | `<SNMP_AUTH_PASSWORD>` or `<SNMP_PRIV_PASSWORD>` differs, or the protocols differ (`sha256` and `aes128` on the controller, `SHA-256` and `AES` in `snmpwalk`) | Re-enter both secrets on the controller; repeat |
| No traps arrive | Community not enabled for v2c traps, wrong host, `snmptrapd` not accepting the community, or P2 lacks UDP 162 | `show switch-controller snmp-community`; `snmptrapd -f -Lo` output; `diagnose sniffer packet any 'udp port 162' 4 5 a` |
| No sFlow datagrams | S1 (no sFlow on the FS-108F); `collector-ip` still `0.0.0.0`; `packet-sampler` not `enabled` on the port; no traffic on the port | `show switch-controller sflow`; the port's `show` in the managed-switch entry; ping from endpoint A |
| No flow records | S1; no collector entry; UDP 2055 not in `lab-svc-174`; flows not yet expired | `diagnose switch-controller switch-info flow-tracking statistics <SWITCH_SN>`; `execute switch-controller switch-action flow-tracking expire-flows-all <SWITCH_SN>` |
| The switch refuses `config system sniffer-profile` | Managed switches may not accept local configuration; S1 has no packet capture | Record it; use the FortiGate sniffer and SPAN instead |
| Endpoint B sees nothing from a mirror | `status inactive`, wrong source or destination, or `tcpdump` filtering VLAN-tagged frames | `get switch mirror status` on the switch; run `tcpdump -e` without a filter |
| RSPAN capture on `rspan` is empty | S1/S2 (no RSPAN); `mode` not `rspan`; no traffic on the source port | `show switch-controller traffic-sniffer` |
| The switch does not return after a fault | The fault was not reverted (cable, mask, detection method, authorization) | Revert in reverse order; `get-conn-status`; restore `fgt-pre-12-4-174.conf` |
| The switch reset itself when it was deauthorized | `switch-on-deauth factory-reset` is in effect on your build (FortiLink Guide, p. 43) | Re-authorize; the entry pushes its configuration back; record it |
| No syslog from the switch | `remote-log` status `disable`; P2 without UDP 514; `rsyslog` listener not loaded | `show switch-controller remote-log`; `~/watch-174.sh`; `ss -lun` on `ubuntu-ws` |
| `diagnose sys ntp status` shows no server | The FortiGate is not serving NTP on the FortiLink port, or its own clock is unsynchronized, or the switch does not take NTP from DHCP (undocumented for this case) | `show system ntp`; `show system dhcp server <FL_DHCP_ID>`; record |
| `set-standalone` leaves the row in `get-conn-status` | Expected: the entry stays until you delete it | Deauthorize and delete the entry |
| The FortiLink interface cannot be changed in the teardown | Objects still refer to it | `diagnose sys cmdb refcnt show system.interface.name <FL_PORT>`; remove the references; `set fortilink disable` |
| The teardown comparison still shows lab objects | A reference you missed, or objects FortiOS created by itself | Remove them, or restore the pre-volume file |
| VLAN 202 does not work on C2 after the teardown | `net2` still has `link_down=1`, the wrong bridge or tag, or `port3`'s VLAN 202 configuration is missing | `qm config 120 \| grep ^net2`; `show system interface port3`; restore `fgt1-pre-174.conf` |

## Security and Best Practices

- **Prefer SNMPv3 with authentication and privacy.** SNMPv1 and v2c send the
  community in clear text; use them only as briefly as Lab 12.2 does, and
  remove the community afterwards. Volume CLXXII asks for SHA-2 authentication
  and AES privacy (its row uses AES-256); the controller offers `aes256` as well
  (FortiLink Guide, p. 304), so use it if your SNMP manager supports it.
- **Open only the path you need.** An SNMP poller needs one policy from the
  poller to the FortiLink port with the `SNMP` service; do not open the whole
  FortiLink subnet, and delete the policy when polling ends.
- **Treat captures as sensitive data.** Packet captures and mirrored traffic
  contain whatever crosses the port, including credentials of clear-text
  protocols. Capture with a filter and a packet limit, delete `.pcap` files on
  the switch when done, and remove mirror sessions; a forgotten SPAN session
  leaks traffic to its destination port.
- **Sample, do not flood.** sFlow and flow export are CPU intensive on the
  switch (FortiLink Guide, p. 308); keep sampling rates at the defaults unless
  you have a reason.
- **Send switch logs off the box.** Keep `switch-log` export to the FortiGate
  and add a remote syslog server; the switch's own log storage is small.
- **Fix the faults you induce.** Revert each fault before inducing the next,
  and confirm `Authorized/Up` each time; never leave a lab FortiLink half
  broken.
- **Retire switches so they cannot be re-adopted by accident.** Use
  `set-standalone`, delete the entry, and reset the switch at its console
  before it leaves your hands; transfer or release its FortiCare registration
  in the support portal if it changes owner.
- **Destroy secrets with the lab.** The RADIUS secret, the switch admin
  password, the SNMPv3 secrets, and the PEAP certificates are lab secrets;
  remove them with the objects and VMs that hold them, and keep the backups on
  VM 140 only as long as you need them, because they contain those secrets in
  encrypted form.

## References and Knowledge Checks

**References**

- [Fortinet, *FortiLink Guide (FortiOS 7.6.7)*](https://docs.fortinet.com/document/fortiswitch/7.6.7/fortilink-guide)
  — supported models and compatibility (p. 12), zero-touch defaults and local
  changes (p. 14), NTP on the FortiLink interface (p. 25), deleting a FortiLink
  interface (p. 33), admin password, `switch-on-deauth`, and console login
  (pp. 43–44), local-access policy (p. 45), `get-conn-status` (p. 52), LLDP
  displays (p. 176), FortiLink secure fabric (pp. 178–182), logging, port
  mirroring, RSPAN, ERSPAN, and the one-arm sniffer (pp. 291–301), SNMP
  (pp. 302–308), sFlow (pp. 308–309), flow tracking and export (pp. 309–313),
  FortiView Internal Hubs (pp. 313–314), names and `get-sync-status`
  (pp. 317–319), deauthorizing and the CSF trusted list (p. 321), standalone
  conversion (p. 322), topology display (pp. 322–324), Diagnostics and Tools,
  cable test, status and fan (pp. 329–333), port display, MAC cache, and port
  statistics (pp. 333–339), configuration sync and firmware (pp. 343–352),
  automatic backups (p. 352).
- [Fortinet, *FortiSwitchOS 7.6.7 CLI Reference*](https://docs.fortinet.com/document/fortiswitch/7.6.7/fortiswitchos-cli-reference)
  — `config system sniffer-profile` (p. 272), `diagnose snmp` (p. 341),
  `diagnose switch fortilink-auth` (p. 352), `diagnose switch mac-address`
  (p. 354), `diagnose switch mclag` (p. 357), `diagnose switch physical-ports
  cable-diag`, `port-stats`, and `summary` (pp. 363, 369, 375), `diagnose
  switch trunk summary` (p. 381), `diagnose sys firmware info` and `flash list`
  (p. 389), `diagnose sys ntp status` (pp. 391–392), `execute factoryreset`
  (p. 420), `execute switch-controller get-conn-status` (p. 451), `execute
  system sniffer-profile` (pp. 459–460), `execute verify image` (p. 464),
  `get switch lldp` (p. 499), `get switch mirror status` (p. 501), `get system
  sniffer-profile` (p. 533), `get system status` (p. 535).
- [Fortinet, *FortiSwitchOS 7.6.7 Administration Guide (Standalone Mode)*](https://docs.fortinet.com/document/fortiswitch/7.6.7/administration-guide)
  — firmware signature warnings (p. 60), packet capture profiles and limits
  (pp. 133–136).
- [Fortinet, FortiOS 7.6 documentation](https://docs.fortinet.com/product/fortigate/7.6)
  — the FortiOS 7.6.0 CLI Reference: `config switch-controller sflow`,
  `flow-tracking`, `snmp-sysinfo`, `snmp-community`, `snmp-user`, `remote-log`,
  `switch-log`, `security-policy local-access`, `traffic-sniffer`,
  `storm-control-policy`, `switch-profile`, `global`, `managed-switch`
  (`mirror`, `ports`, `access-profile`), `config system ntp`, `config system
  dhcp server`, `config firewall policy`.
- FortiOS 8.0.1 CLI Reference (cross-check only) — `diagnose sniffer packet`,
  `diagnose switch-controller switch-info mac-table`, `execute switch-controller
  switch-action cable-diag`, `switch-software delete`, `execute backup config`,
  `execute restore config`, `diagnose sys cmdb refcnt`.
- FortiSwitchOS 7.6.7 feature matrix (`temp/fsw/FSW-7.6.7-Feature-Matrix.pdf`)
  — the rows in this chapter's model table; note 17.
- [Volume CLXXII, Chapter 11](../../volume-172-disa-srgs-and-stigs/chapters/11-fortiswitch-feature-version-and-srg-map.md)
  — prerequisites P1, P4–P7, P10, P12, P13, P18, and the feature-row commands
  that Lab 12.5 re-checks; [Chapter 33](../../volume-172-disa-srgs-and-stigs/chapters/33-fortiswitch-and-cisco-catalyst-switch-stig-crosswalk.md)
  — the Layer 2 rules of Lab 8.5 Part D.
- [Proxmox VE, *PCI(e) Passthrough*](https://pve.proxmox.com/wiki/PCI(e)_Passthrough)
  and the [`qm(1)` manual](https://pve.proxmox.com/pve-docs/qm.1.html) —
  `--net[n]`, `--delete`, `hostpci`, `destroy`.
- [`snmpwalk(1)`](https://manpages.ubuntu.com/manpages/noble/man1/snmpwalk.1.html),
  [`snmpcmd(1)`](https://manpages.ubuntu.com/manpages/noble/man1/snmpcmd.1.html),
  [`snmptrapd(8)`](https://manpages.ubuntu.com/manpages/noble/man8/snmptrapd.8.html),
  [`snmptrapd.conf(5)`](https://manpages.ubuntu.com/manpages/noble/man5/snmptrapd.conf.5.html),
  [`tcpdump(8)`](https://manpages.ubuntu.com/manpages/noble/man8/tcpdump.8.html),
  [`picocom(1)`](https://manpages.ubuntu.com/manpages/noble/man1/picocom.1.html).
- [Volume XXVI, Chapter 05](../../volume-026-proxmox-lab-poweredge-r640/chapters/05-network-architecture-management-nic-vlan-trunk-and-bridges.md)
  — Proxmox bridges and `ifreload -a`; [Volume CM, Chapter 04](../../volume-900-tims-lab-gear/chapters/04-current-device-configurations.md)
  — the Nexus access-port pattern.

**Knowledge checks**

1. Which view of a managed switch still works when the FortiLink session is
   down, and which command would you use to read the switch's MAC table from
   it?
2. An SNMP manager on the services segment cannot poll a managed switch,
   although the switch sends traps to the same manager. Name the two things
   that differ between the trap path and the polling path.
3. Why does Lab 12.2 add UDP 2055 to `lab-svc-174` but not create a new policy
   for flow export, while SNMP polling needs P3?
4. Which switch options in this volume can run an on-switch packet capture, and
   which can send RSPAN to the controller? Where does the controller receive
   RSPAN traffic?
5. A switch row reads `Authorized/Down` with ADDRESS `0.0.0.0`, and the topology
   view shows a dashed line with a broken-link icon. Name two causes the
   FortiLink Guide gives, and the first check for each.
6. You change the FortiLink interface's neighbor detection while a switch is
   managed. What did you record about the switch's session, and why is that a
   recorded result rather than a documented one?
7. Which Volume CLXXII prerequisites cannot be met in FortiLink mode on this
   volume's switches, and which feature matrix marks say so?
8. Why does the teardown retire `FSW-B` before `FSW-A` on S3?
9. What is the difference between restoring `fgt1-pre-174.conf` and removing the
   lab objects by hand, and which steps of the teardown are needed on both
   paths?
10. Which file on VM 140 is the pre-volume configuration for each controller
    option?

## Hands-On Lab

**Shared prerequisites.** Chapter 11 complete (ADDENDUM 11 state):
`<SWITCH_SN>` `Authorized/Up` at `10.255.1.2` (or the address Lab 11.5
recorded), description `FSW-A lab-174`, profile `fsw-174-prof`, the Lab 3.3
build, and the Chapter 10 port and STP settings: `port1` native `fsw-users`
(endpoint A, DHCP, BPDU guard, allowed list `<PORT1_ALLOWED>`), `port2` native
`fsw-iot` (endpoint B, `10.174.43.20/24`, allowed list `<PORT2_ALLOWED>`),
`port4` up with no description, `port5` with the loop cable (other end loose),
`port3` unplugged. On S3, `FSW-B` (`<FSWB_SN>`) managed behind the MCLAG ICL on
`FSW-A` `port23`/`port24`. The controller in single-VDOM mode, with the
Chapter 04 VLAN interfaces, zone `FSW-LAN`, P1 and P2, and on C2 P3 free;
`disable-discovery` does not list the switch. `ubuntu-ws` runs the rsyslog UDP
listener from Lab 2.5. The Nexus port used in Chapters 02 and 11 is shut.
Endpoints have `tcpdump`; endpoint B has `iperf`. VM 140 holds every backup
listed in Design Considerations. Track 2: the controller, the stand-in entry
`S248EPTF18000000` if Lab 2.2's outcome allowed it, and `radius-174`.
**Cost:** none.

`FGT #` is the controller on any option and `FSW #` the switch console. Blocks
written for `port3` apply to C3 with `port4` and to C1 with `<FL_PORT>`. On S3,
`FSW #` is `FSW-A` unless a step names `FSW-B`.

### Lab 12.1 — Read the switch from both sides

**Objective:** Read a managed switch's MAC table, LLDP neighbors, port
statistics, cable state, physical connections, and topology from the
controller and from the switch, and match each controller view to the switch
command that shows the same thing.

**Platform notes:** Hands-on on C1, C2, and C3 with S1, S2, or S3 (on S3, run
the switch commands on `FSW-A`; the topology views also show `FSW-B`). Port
names are the same on every switch option. `switch-info status` and
`switch-info fan` need FortiOS 7.6.3 or later, so they are read-only on FGT-1
(7.6.2); a C1 or C3 on 7.6.3 or later runs them. Track 2: read-and-predict.

**Track 1:**

1. Generate known traffic. On endpoint A, ping the `fsw-users` gateway, and on
   endpoint B the `fsw-iot` gateway, and leave both running:

   ```bash
   # endpoint A
   ping 10.174.41.1
   # endpoint B
   ping 10.174.43.1
   ```

2. Read the MAC table from the switch, then from the controller. The
   controller command is in the FortiOS 8.0.1 CLI Reference (with a VLAN
   argument) but not in the FortiLink Guide 7.6.7; type `?` after
   `mac-table` on your build and record the arguments it accepts. The MAC
   cache command is the guide's (p. 334):

   ```text
   FSW # diagnose switch mac-address list
   FGT # diagnose switch-controller switch-info mac-table <SWITCH_SN>
   FGT # diagnose switch-controller mac-cache show <SWITCH_SN>
   ```

   Predict the switch's entries for the two endpoints. **Answer:** `<MAC_A>` in
   VLAN 1741 on `port1` and `<MAC_B>` in VLAN 1743 on `port2`, each with its
   flags, plus the switch's own `internal` entry in VLAN 4094 (the shape of the
   CLI Reference example, p. 354, which shows `internal` in VLAN 4094 with the
   `static` flag). Record whether the FortiGate's MAC address appears on the
   FortiLink trunk `<FL_TRUNK>` in VLANs 1741 and 1743.

3. Read the LLDP neighbors from both sides:

   ```text
   FGT # diagnose switch-controller switch-info lldp neighbors-summary <SWITCH_SN>
   FGT # diagnose switch-controller switch-info lldp neighbors-detail <SWITCH_SN>
   FSW # get switch lldp neighbors-summary
   ```

   Predict which ports list a neighbor. **Answer:** `<FSW_FL_PORT>`, with the
   controller as its neighbor, because the FortiLink interface transmits LLDP
   (`lldp-transmission enable`, Lab 2.2); on S3 also `port23` and `port24`
   (`FSW-B`). The endpoints send no LLDP (Chapter 10 removed `lldpd`), so
   `port1` and `port2` list none.

4. Read the physical connections and the switch's own session view:

   ```text
   FGT # execute switch-controller get-physical-conn standard port3
   FGT # execute switch-controller get-conn-status
   FSW # execute switch-controller get-conn-status
   ```

   Then open **WiFi & Switch Controller > Managed FortiSwitches**, choose the
   **Topology** view, and compare it with the text: a solid green line from
   the FortiLink interface to the switch (and on S3 between the switches) means
   the links are up (FortiLink Guide 7.6.7, p. 322). Open **Security Fabric >
   Physical Topology** as well.

5. Read port statistics, reset them, and read them again. The reset is a
   debugging aid; the guide warns that counters gathered during a reset may be
   discarded and that SNMP and FortiGate monitoring can be affected (p. 338):

   ```text
   FGT # diagnose switch-controller switch-info port-stats <SWITCH_SN> port1
   FSW # diagnose switch physical-ports summary port1
   FGT # diagnose switch-controller trigger reset-hardware-counters <SWITCH_SN> port1
   FGT # diagnose switch-controller switch-info port-stats <SWITCH_SN> port1
   FGT # diagnose switch-controller trigger restore-hardware-counters <SWITCH_SN> port1
   FGT # diagnose switch-controller switch-info port-stats <SWITCH_SN> port1
   ```

   Predict the second reading. **Answer:** small counts that grow with the
   ping (one echo request a second in, one reply a second out), because the
   counters were zeroed; after `restore-hardware-counters` the totals return.
   The guide does not say whether the restore adds the packets counted during
   the reset; record what you see.

6. Read the port's properties and run a cable test on the unused `port4`. A
   cable test on a port whose link is up interrupts its traffic for several
   seconds (p. 331), which is why the test uses a port with nothing plugged in:

   ```text
   FGT # diagnose switch-controller switch-info port-properties <SWITCH_SN> port1
   FGT # execute switch-controller switch-action cable-diag <SWITCH_SN> port4
   FSW # diagnose switch physical-ports cable-diag port4
   ```

   Predict the result for `port4`. **Answer:** every pair `Open`, length 0
   meters: the guide says an unconnected port reads `Open` with length 0
   (p. 331), and the CLI Reference example shows four open pairs (p. 363). On an
   FS-124E or FS-148E model the guide lists limitations (no crosstalk, a
   five-second delay, inaccurate lengths, p. 332); they do not apply to S1 or
   S2.

7. On C1 or C3 with FortiOS 7.6.3 or later only, read the hardware status and
   the fans. On FGT-1 (7.6.2), read the guide's example instead and skip the
   commands:

   ```text
   FGT # diagnose switch-controller switch-info status
   FGT # diagnose switch-controller switch-info fan <SWITCH_SN>
   ```

   Compare `Firmware Signature` in the status output with `get system status`
   on the switch. Stop the two pings.

**Track 2: read-and-predict.**

1. The FortiLink Guide (p. 336) shows `port-stats` for a port that reads
   `Port(port8) is Admin up, line protocol is down`, `half-duplex, 0 Mb/s`, and
   zero input and output packets. Predict the cause. **Answer:** nothing is
   linked on the port: it is enabled (`Admin up`) but has no carrier, so no
   speed or duplex was negotiated and no frames were counted.
2. The CLI Reference (p. 354) lists `MAC: 08:5b:0e:f1:95:e5 VLAN: 4094 Port:
   internal(port-id 31)`. Predict what this entry is. **Answer:** the switch's
   own management address on its internal interface in the FortiLink
   management VLAN 4094 (the default `switch-controller-mgmt-vlan`), marked
   `static`; it is how the controller reaches the switch.
3. A managed switch shows no LLDP neighbor on its FortiLink port. Predict two
   causes from this volume. **Answer:** the FortiLink interface does not
   transmit LLDP (`lldp-transmission disable`), or a bridge between them drops
   LLDP (Chapter 02's `group_fwd_mask`).
4. Run `execute switch-controller get-conn-status` and `execute
   switch-controller get-physical-conn standard port3` on your controller.
   Record the output for a FortiLink port with no switch: the `get-conn-status`
   table has no Up row, and the stand-in entry (if it exists) has no address.

**Expected result:** Track 1: the MAC table lists both endpoints on the right
ports and VLANs on the switch and through the controller (or the controller
command's accepted syntax is recorded); LLDP lists the controller on
`<FSW_FL_PORT>` (and `FSW-B` on S3); `get-physical-conn` and the topology view
agree; port statistics were read, reset, and restored; `port4` tested `Open`
with length 0. Track 2: the predictions are answered and the empty
`get-conn-status` output is recorded.

**Negative test:** Ask the controller for the MAC cache of a switch that does
not exist:

```text
FGT # diagnose switch-controller mac-cache show S124EN5918003682
```

The guide prints no error for this case; record what FortiOS returns (an error
or an empty table). On Track 2, run the same command against
`S248EPTF18000000`.

**Rollback:** None needed: the lab changed nothing except the port counters,
which step 5 restored. Stop the pings on both endpoints.

**Lab verified by:** *pending*

### Lab 12.2 — SNMP, sFlow, and flow export to the collector

**Objective:** Poll the switch with SNMPv3, receive an SNMP trap, and send
sFlow samples and flow records to `ubuntu-ws`, using P2 for everything the
switch sends and P3 for the one query path.

**Platform notes:** Hands-on on C1, C2, and C3 with S1, S2, or S3 (on S3,
`FSW-A`). SNMP is live on every switch option. sFlow and flow export are live
on S2 and S3 and read-and-predict on S1 (the FS-108F is not in the 1xxE/1xxF
model lists for sFlow or flow export). On C2 the SNMP polling policy is P3, the
last free slot; on C1 it uses source NAT, because `ubuntu-ws` routes through
FGT-1, not through C1. FortiView Internal Hubs is described, not built (dash in
1xxE/1xxF, and it needs a FortiGate with a hard disk). Track 2: build the
controller objects, then read-and-predict.

**Track 1, Part A — the collector and the SNMP objects:**

1. Back up the controller:

   ```text
   FGT # execute backup config tftp fgt-pre-12-2-174.conf 10.30.99.50
   ```

2. On `ubuntu-ws`, install the SNMP tools and the trap receiver, and save the
   watcher script from Implementation and Automation. Record which packages you
   installed, because Lab 12.6 removes them:

   ```bash
   # ubuntu-ws
   sudo apt update && sudo apt install -y snmp snmptrapd tcpdump
   chmod +x ~/watch-174.sh
   ```

3. Read the starting state of the controller's switch-SNMP and access objects,
   so that Lab 12.6 can return them:

   ```text
   FGT # show switch-controller snmp-sysinfo
   FGT # show switch-controller snmp-community
   FGT # show switch-controller snmp-user
   FGT # show switch-controller security-policy local-access
   FGT # show switch-controller sflow
   FGT # show switch-controller flow-tracking
   ```

4. Enable the switch SNMP agent and create the SNMPv3 user. Use secrets of at
   least eight characters:

   ```text
   FGT # config switch-controller snmp-sysinfo
   set status enable
   set description "lab-174 managed switch"
   set contact-info "lab-174"
   set location "lab-174 rack"
   end
   FGT # config switch-controller snmp-user
   edit "snmp-174"
   set queries enable
   set security-level auth-priv
   set auth-proto sha256
   set auth-pwd <SNMP_AUTH_PASSWORD>
   set priv-proto aes128
   set priv-pwd <SNMP_PRIV_PASSWORD>
   next
   end
   ```

5. Allow SNMP on the switch's internal interface with a local-access policy of
   its own, and bind it. The guide adds `snmp` to `internal-allowaccess` for
   polling (p. 303); the policy leaves out HTTP and Telnet, which Lab 12.5
   counts as part of the hardening:

   ```text
   FGT # config switch-controller security-policy local-access
   edit "la-174"
   set mgmt-allowaccess https ping ssh
   set internal-allowaccess https ping ssh snmp
   next
   end
   FGT # config switch-controller managed-switch
   edit <SWITCH_SN>
   set access-profile "la-174"
   next
   end
   ```

6. Add the polling policy. **C2 and C3** (C3 with `port4`):

   ```text
   FGT # config firewall policy
   edit 0
   set name "P3-snmp-174"
   set srcintf "port2"
   set dstintf "port3"
   set srcaddr "ubuntu-ws"
   set dstaddr "all"
   set action accept
   set schedule "always"
   set service "SNMP"
   set logtraffic all
   next
   end
   ```

   **C1:** the same policy with `srcintf "<SVC_PORT>"`, `dstintf "<FL_PORT>"`,
   and `set nat enable`, so that the switch's replies return to C1 rather than
   to FGT-1, which is `ubuntu-ws`'s gateway. Record the new policy's ID as
   `<P3_ID>`.

**Track 1, Part B — SNMPv3 queries and a trap:**

7. Poll the switch's system group from `ubuntu-ws`. `-a SHA-256` and `-x AES`
   (AES-128) match the controller's `sha256` and `aes128` (`snmpcmd(1)`); the
   numeric OID avoids any MIB files:

   ```bash
   # ubuntu-ws
   snmpwalk -v3 -l authPriv -u snmp-174 -a SHA-256 -A '<SNMP_AUTH_PASSWORD>' \
     -x AES -X '<SNMP_PRIV_PASSWORD>' 10.255.1.2 1.3.6.1.2.1.1
   ```

   Predict two of the values. **Answer:** `sysContact` reads `lab-174` and
   `sysLocation` reads `lab-174 rack`, the strings from step 4, if the
   controller pushes them as the guide describes; `sysDescr` is the
   description you set or the switch's own text. Record the output.

8. Add a v2c trap community for the trap test. The managed switch's SNMPv3 user
   has no notification host in the FortiOS 7.6.0 CLI Reference, so this lab
   uses v2c traps and removes the community again in Lab 12.5:

   ```text
   FGT # config switch-controller snmp-community
   edit 1
   set name "trap-174"
   set status enable
   set query-v1-status disable
   set query-v2c-status disable
   set trap-v1-status disable
   set trap-v2c-status enable
   config hosts
   edit 1
   set ip 10.200.0.20
   next
   end
   next
   end
   ```

9. Receive the trap. On `ubuntu-ws`, let `snmptrapd` accept the community and
   run it in the foreground, logging to the terminal (`snmptrapd(8)`,
   `snmptrapd.conf(5)`):

   ```bash
   # ubuntu-ws
   echo 'authCommunity log trap-174' | sudo tee -a /etc/snmp/snmptrapd.conf
   sudo systemctl stop snmptrapd
   sudo snmptrapd -f -Lo
   ```

   On the switch console, generate a trap (CLI Reference, p. 341):

   ```text
   FSW # diagnose snmp trap send
   ```

   Record what `snmptrapd` prints. If nothing arrives, check the path with the
   FortiGate sniffer (Lab 12.3) on UDP 162, and record whether the switch sent
   anything. Stop `snmptrapd` with Ctrl+C.

10. Optional (FortiOS 7.6.0 and later, p. 306): ask for MAC-change traps on the
    same community and log dynamic MAC events on `port1` (a static-access
    port), then unplug and replug endpoint A and watch `snmptrapd` again. The
    guide warns that MAC events can be lost by the hardware or software:

    ```text
    FGT # config switch-controller snmp-community
    edit 1
    append events l2mac
    next
    end
    FGT # config switch-controller managed-switch
    edit <SWITCH_SN>
    config ports
    edit "port1"
    set log-mac-event enable
    next
    end
    next
    end
    ```

**Track 1, Part C — sFlow (S2 and S3):**

11. Point the controller's sFlow collector at `ubuntu-ws` and sample `port1`.
    The guide prints the collector lines without `set` (p. 308); the FortiOS
    7.6.0 reference has the `set` form used here. The FortiOS 7.6.0 default
    packet sample rate is 512:

    ```text
    FGT # config switch-controller sflow
    set collector-ip 10.200.0.20
    set collector-port 6343
    end
    FGT # config switch-controller managed-switch
    edit <SWITCH_SN>
    config ports
    edit "port1"
    set packet-sampler enabled
    set packet-sample-rate 512
    set sflow-counter-interval 30
    next
    end
    next
    end
    ```

12. Start a fast ping from endpoint A to its gateway, then run the watcher on
    `ubuntu-ws` and look at the UDP 6343 section:

    ```bash
    # endpoint A
    sudo ping -i 0.01 -c 3000 10.174.41.1
    # ubuntu-ws
    ~/watch-174.sh
    ```

    Predict what arrives. **Answer:** UDP datagrams from `10.255.1.2` to port
    6343: counter samples about every 30 seconds (`sflow-counter-interval 30`)
    and flow samples while the ping runs. They pass because P2 allows UDP 6343
    from the FortiLink port to `ubuntu-ws`. `tcpdump` shows only that datagrams
    arrive; to read the samples, use an sFlow decoder of your choice and record
    which one.

**Track 1, Part D — flow export (S2 and S3):**

13. Let P2 carry flow export, then add a collector. `sample-mode perimeter`,
    `format netflow9`, and `level ip` are the FortiOS 7.6.0 defaults, so only
    the collector is set; the guide asks for packet sampling on the ports
    first (p. 310), which step 11 enabled on `port1`:

    ```text
    FGT # config firewall service custom
    edit "lab-svc-174"
    set udp-portrange 1812-1813 514 162 6343 2055
    next
    end
    FGT # config switch-controller flow-tracking
    config collectors
    edit "ws-174"
    set ip 10.200.0.20
    set port 2055
    set transport udp
    next
    end
    end
    ```

14. Repeat the fast ping from endpoint A, expire the flows so that the switch
    exports them now (p. 312), and read the switch's flow view:

    ```text
    FGT # execute switch-controller switch-action flow-tracking expire-flows-all <SWITCH_SN>
    FGT # diagnose switch-controller switch-info flow-tracking statistics <SWITCH_SN>
    FGT # diagnose switch-controller switch-info flow-tracking flows 10 all <SWITCH_SN> port1
    ```

    On `ubuntu-ws`, run `~/watch-174.sh` and look at the UDP 2055 section.
    Record which ports the flows came from: the guide and the 7.6.0 reference
    describe perimeter mode differently (Theory and Architecture). If no flows
    arrive while sFlow is configured, the documents do not say whether both can
    sample a port at once: set the sFlow `collector-ip` back to `0.0.0.0`,
    repeat, and record the result.

15. Note what the controller's own flow collector reports. It belongs to
    FortiView Internal Hubs (collector address equal to the FortiLink
    interface, a hard disk, and historical FortiView; pp. 313–314), which this
    lab does not build, so expect it to be disabled:

    ```text
    FGT # diagnose switch-controller flow-collector status
    ```

**Track 2:** Do steps 1, 3–6, 8, 11 (the collector only; the per-port lines
too, against `S248EPTF18000000`, if Lab 2.2's third outcome applies), and 13 on
your controller, and check each with its `show` command. On FGT-1 alone, P3 is
free for step 6. The SNMP walk, the trap, and the samples need a switch.

**Track 2: read-and-predict.**

1. The FortiLink Guide (p. 308) queries a FortiGate at `172.16.200.1` with
   `snmpwalk -v2c -c REGR-SYS` for OID `1.3.6.1.4.1.12356.101.24.1.1.1.11` and a
   serial-derived suffix. Predict what the value is and which device answers.
   **Answer:** the percentage of CPU in use on the managed switch
   (`fgSwCpu`), answered by the **FortiGate's** SNMP agent, which reports its
   switches' statistics; the switch updates them every 30 seconds (p. 307).
2. The guide's example of `diagnose switch-controller flow-collector status`
   (p. 313) shows `status : enabled`, `interface : port11`, and `flows : 42`.
   Predict what `interface` names. **Answer:** the FortiLink interface on which
   the FortiGate collects the switches' flows for FortiView Internal Hubs.
3. Predict whether an FS-108F sends sFlow samples after step 11. **Answer:** no.
   The feature matrix lists sFlow in the 1xxE/1xxF column only for the FS-124F,
   FS-148E, and FS-148F, so the controller may accept the configuration but the
   switch has nothing to send; record what `show` reports on S1.

**Expected result:** Track 1: `snmpwalk` returns the system group with the
strings from step 4; a trap from `10.255.1.2` reached `snmptrapd` (or its
absence is recorded with the sniffer result); on S2 and S3, sFlow datagrams and
flow records from `10.255.1.2` reached `ubuntu-ws`, and the flow statistics
show exported flows. On C2 all three policy slots are in use. Track 2: the
objects exist and the predictions are answered.

**Negative test:** Disable P3 and poll again, then enable it:

```text
FGT # config firewall policy
edit <P3_ID>
set status disable
next
end
```

`snmpwalk` times out, because nothing allows UDP 161 from `ubuntu-ws` to the
FortiLink port. Then poll with a wrong `-X` secret while P3 is enabled again
(`set status enable`): `snmpwalk` reports an error or times out; record which.
Track 2: confirm with `show firewall policy <P3_ID>` that the policy is
disabled and enabled again.

**Rollback:** Keep everything for Labs 12.3–12.5; Lab 12.5 removes the v2c
community, and Lab 12.6 removes the rest. To undo only this lab, delete P3,
the community, `snmp-174`, `ws-174`, and `la-174` (after `set access-profile
"default"` on the entry), set the sFlow `collector-ip` back to `0.0.0.0`,
disable the samplers and `log-mac-event` on `port1`, return `snmp-sysinfo` and
`lab-svc-174` to step 3's values, or restore `fgt-pre-12-2-174.conf`.

**Lab verified by:** *pending*

### Lab 12.3 — Capture traffic four ways

**Objective:** Capture the switch's management and user traffic with the
FortiGate sniffer, capture user traffic on the switch itself, mirror a port to
an analyzer port, and send mirrored traffic to the controller with RSPAN.

**Platform notes:** The FortiGate sniffer (Part A) is hands-on on every option,
Track 2 included (on Track 2, on `port2` with RADIUS traffic). On-switch capture
(Part B) is hands-on on S2 and S3 and read-and-predict on S1. SPAN (Part C) is
hands-on on S1, S2, and S3. RSPAN (Part D) is hands-on on S3 only and
read-and-predict on S1 and S2 (dash in 1xxE/1xxF). The standalone mirror
(Part E) is read-and-predict on every option, because the switch is managed.
No policy is added.

**Track 1, Part A — the FortiGate sniffer:**

1. Capture the switch's traffic on the FortiLink port (C3: `port4`; C1:
   `<FL_PORT>`). Verbose level 4 prints headers with the interface name; `a`
   prints absolute timestamps (FortiOS 8.0.1 CLI Reference, cross-check):

   ```text
   FGT # diagnose sniffer packet port3 'host 10.255.1.2' 4 20 a
   ```

   Record the protocols and ports you see between `10.255.1.1` and
   `10.255.1.2`. The local documents say the management session is CAPWAP by
   default or HTTPS (FortiLink Guide 7.6.7, p. 50) but do not list its ports,
   so the capture is your record.

2. Capture user traffic on a VLAN interface while endpoint A pings its gateway,
   then follow an export through the controller with the `any` interface:

   ```text
   FGT # diagnose sniffer packet fsw-users 'icmp' 4 6 a
   FGT # diagnose sniffer packet any 'udp port 6343' 4 6 a
   ```

   Predict the interfaces in the second capture (S2 and S3, with Lab 12.2's
   sFlow running). **Answer:** each datagram twice: in on `port3` (from
   `10.255.1.2`) and out on `port2` (to `10.200.0.20`), because P2 forwards it
   from the FortiLink port to the services segment.

**Track 1, Part B — capture on the switch (S2 and S3):**

3. Create a capture profile on the switch console for ICMP on `port1`, start
   it, ping from endpoint A, and stop it (Administration Guide, pp. 133–136;
   CLI Reference, pp. 272, 459–460, 533). The profile is a local change on a
   managed switch, which the controller does not know about (FortiLink Guide,
   p. 14); record whether the switch accepts it:

   ```text
   FSW # config system sniffer-profile
   edit "cap-174"
   set filter "icmp"
   set max-pkt-count 20
   set max-pkt-len 128
   set switch-interface "port1"
   next
   end
   FSW # execute system sniffer-profile start cap-174
   FSW # get system sniffer-profile summary
   ```

   ```bash
   # endpoint A
   ping -c 10 10.174.41.1
   ```

   ```text
   FSW # execute system sniffer-profile stop cap-174
   FSW # get system sniffer-profile capture cap-174
   ```

   Predict the summary line after the stop. **Answer:** profile `cap-174`,
   status `Stop`, a packet count of up to 20 (ten echo requests and ten replies
   if both directions are captured on `port1`), snap length 128, and filter
   `icmp` (the columns of the CLI Reference example, p. 534).

4. Delete the capture and the profile. A `.pcap` file can be deleted only
   after the capture is stopped (Administration Guide, p. 136). Uploading it
   with `execute system sniffer-profile upload tftp` would need a policy from
   the FortiLink port to VM 140, which C2 cannot afford, so this lab reads the
   capture on the console only:

   ```text
   FSW # execute system sniffer-profile delete-capture cap-174
   FSW # config system sniffer-profile
   delete "cap-174"
   end
   ```

**Track 1, Part C — mirror a port (SPAN):**

5. Mirror what enters `port1` (endpoint A) to `port2` (endpoint B), keeping
   normal switching on `port2` (`switching-packet enable`, FortiLink Guide,
   p. 293). Run `tcpdump` on endpoint B without a filter, so that tagged frames
   are not filtered out, and ping from endpoint A:

   ```text
   FGT # config switch-controller managed-switch
   edit <SWITCH_SN>
   config mirror
   edit "mir-174"
   set status active
   set dst "port2"
   set switching-packet enable
   set src-ingress "port1"
   next
   end
   next
   end
   FSW # get switch mirror status
   ```

   ```bash
   # endpoint B
   sudo tcpdump -e -n -i <IFACE_B> -c 20
   # endpoint A
   ping -c 5 10.174.41.1
   ```

   Predict what endpoint B sees. **Answer:** endpoint A's echo requests to
   `10.174.41.1`, with endpoint A's MAC address as the source, although
   endpoint B is in another VLAN: a mirror copies frames regardless of VLAN.
   Record whether the copies carry an 802.1Q tag for VLAN 1741; the switch's
   standalone `strip-mirrored-traffic-tags` option (CLI Reference, p. 149)
   suggests both are possible, and the FortiLink Guide does not say which a
   managed mirror does. Endpoint B's own ping to its gateway keeps working.

6. Remove the mirror:

   ```text
   FGT # config switch-controller managed-switch
   edit <SWITCH_SN>
   config mirror
   delete "mir-174"
   end
   next
   end
   ```

**Track 1, Part D — RSPAN to the controller (S3):**

7. Mirror `port1` ingress into the RSPAN VLAN and capture it on the controller's
   `rspan` interface (VLAN 4092, an auto-created interface; FortiLink Guide,
   pp. 293–295):

   ```text
   FGT # config switch-controller traffic-sniffer
   set mode rspan
   config target-port
   edit <SWITCH_SN>
   set description "rspan-174"
   set in-ports "port1"
   next
   end
   end
   FGT # diagnose sniffer packet rspan 'icmp' 4 10 a
   FGT # show switch-controller traffic-policy
   ```

   Ping from endpoint A while the sniffer runs. Predict two things. **Answer:**
   the sniffer shows endpoint A's echo requests arriving on `rspan`; and a
   traffic policy named `sniffer` now exists, the policer the switch controller
   adds for RSPAN (p. 293). Record its values.

8. Turn RSPAN off and remove the target (`set mode none`, p. 294):

   ```text
   FGT # config switch-controller traffic-sniffer
   config target-port
   delete <SWITCH_SN>
   end
   set mode none
   end
   ```

**Track 2:** Run Part A on `port2` while you repeat Lab 2.5's RADIUS test in a
second session, so that the capture has traffic:

```text
FGT # diagnose sniffer packet port2 'udp port 1812' 4 4 a
FGT # diagnose test authserver radius radius-174 pap labuser <LAB_PASSWORD>
```

Predict the packets. **Answer:** an Access-Request from `10.200.0.1` (C1:
`10.200.0.175`) to `10.200.0.174` port 1812 and the Access-Accept back. Then do
the read-and-predict items.

**Track 2: read-and-predict.**

1. An FS-108F is managed and you create `cap-174` on its console. Predict the
   result. **Answer:** no capture. The feature matrix lists packet capture in
   the 1xxE/1xxF column only for the FS-124F, FS-148E, and FS-148F; the
   Administration Guide's profile table likewise names only those 1xx models.
2. The guide's RSPAN example (p. 295) mirrors traffic from MAC
   `00:00:00:aa:bb:cc`, from IP `10.254.254.192`, and on `port5`–`port7` (in)
   and `port10` (out) of `S524DF4K15000024`. Predict where an administrator
   captures it. **Answer:** on the FortiGate's `rspan` VLAN interface
   (**Network > Diagnostics > Packet Capture**, or `diagnose sniffer packet
   rspan`), because RSPAN carries the copies in VLAN 4092 to the FortiGate.
3. An administrator wants both SPAN to a local analyzer and ERSPAN to a remote
   collector on the same switch. Predict the outcome. **Answer:** not possible:
   ERSPAN cannot be used with SPAN or RSPAN (p. 293).
4. **Part E, the standalone mirror.** In standalone mode the same switch would
   mirror with `config switch mirror`, `set mode SPAN`, `set dst`, `set
   src-ingress`, and `set status active` (CLI Reference, pp. 148–149). Predict
   why this lab does not type it on the managed switch. **Answer:** the switch's
   configuration belongs to the controller in FortiLink mode; the controller's
   `config mirror` is the managed equivalent, and a local change would be
   unknown to the FortiGate and lost at the next restart (FortiLink Guide,
   p. 14).

**Expected result:** Track 1: the FortiLink-port capture shows the management
session's protocols (recorded); `fsw-users` shows endpoint A's ICMP; the `any`
capture shows sFlow in on the FortiLink port and out on `port2` (S2, S3); on S2
and S3 the switch captured endpoint A's ICMP on `port1` (or its refusal is
recorded), and the profile is gone; endpoint B saw endpoint A's mirrored
frames, and the mirror is gone; on S3 the `rspan` capture showed endpoint A's
frames, and RSPAN is off. Track 2: the RADIUS exchange was captured and the
predictions are answered.

**Negative test:** Start a capture on a profile that does not exist on the
switch, and capture on the controller with a filter that matches nothing:

```text
FSW # execute system sniffer-profile start no-such-174
FGT # diagnose sniffer packet port3 'host 192.0.2.99' 4 5 a
```

The switch refuses the first (record the message), and the sniffer prints no
packets until you stop it with Ctrl+C (`192.0.2.99` is a documentation address
that nothing in the lab uses). Track 2: run the second command on `port2`.

**Rollback:** Parts B to D already removed what they created. Check that
nothing is left:

```text
FSW # get system sniffer-profile summary
FGT # show switch-controller traffic-sniffer
FGT # show switch-controller managed-switch <SWITCH_SN>
```

The summary lists no `cap-174`, the traffic sniffer is in mode `none` (or
shows no settings), and the entry has no `config mirror` block.

**Lab verified by:** *pending*

### Lab 12.4 — FortiLink fault clinic

**Objective:** Induce the common FortiLink faults one at a time, record the
signature each leaves in the controller's and the switch's views, revert it,
and predict the signatures of the faults that are too costly to induce.

**Platform notes:** Faults 1, 3, and 4 are hands-on on C1, C2, and C3 with S1,
S2, or S3. Fault 2 is hands-on everywhere, but the method differs: on C2 and C3
with Option A (`vmbrFL`) you clear the bridge's `group_fwd_mask`; on C1 and on
Option B (passthrough) you turn off LLDP reception on the FortiLink interface.
Fault 7 (an inter-switch link member) is hands-on on S3 only and
read-and-predict on S1 and S2. Faults 5 (wrong VDOM) and 6 (incompatible
firmware) are read-and-predict on every option: C2 has one traffic VDOM
(Chapter 10), and the lab never downgrades firmware. Each fault takes the
switch offline for a few minutes; on S3, `FSW-B` goes down with `FSW-A`
whenever `FSW-A` loses the controller. Allow about 90 minutes. Track 2:
read-and-predict, plus the baseline commands on the unlinked FortiLink port.

**Track 1 — baseline:**

1. Back up the controller and start a console log on the switch
   (`picocom --logfile`, as in Chapter 11):

   ```text
   FGT # execute backup config tftp fgt-pre-12-4-174.conf 10.30.99.50
   ```

2. Record the healthy state from both sides. Compare `get-sync-status` with the
   in-sync fields Lab 3.4 recorded:

   ```text
   FGT # execute switch-controller get-conn-status
   FGT # execute switch-controller get-physical-conn standard port3
   FGT # diagnose switch-controller switch-info lldp neighbors-summary <SWITCH_SN>
   FGT # execute switch-controller get-sync-status all
   FGT # get switch-controller global
   FSW # execute switch-controller get-conn-status
   FSW # diagnose switch trunk summary
   FSW # diagnose switch fortilink-auth status <FSW_FL_PORT>
   ```

   In the `get switch-controller global` output, look for `switch-on-deauth`
   (FortiLink Guide 7.6.7, p. 43; not in the FortiOS 7.6.0 CLI Reference).
   Inside `config switch-controller global`, type `set switch-on-deauth ?`
   and leave with `abort`; record whether the option exists and its value. It
   decides what fault 4 does to the switch. The `fortilink-auth` line is the
   secure-fabric baseline: this volume never enabled the secure fabric, so
   record the state it reports for an unauthenticated port.

**Track 1 — fault 1, the FortiLink cable:**

3. Unplug the FortiLink cable at `<FSW_FL_PORT>`. Run `get-conn-status` on the
   controller every 30 seconds and the switch's own `get-conn-status` on the
   console, and watch the **Topology** view:

   ```text
   FGT # execute switch-controller get-conn-status
   FSW # execute switch-controller get-conn-status
   ```

   Predict the controller's row once it notices. **Answer:** `Authorized/Down`
   with ADDRESS `0.0.0.0` (the shape of the guide's example, p. 348), and a
   dashed line with a broken-link icon in the topology (p. 323). The
   authorization is kept, because the entry still has `fsw-wan1-admin enable`.
   Record how long the controller took to show `Down`.

4. Plug the cable back in. Record how long the switch takes to return to
   `Authorized/Up` and whether FLAG `C` appears on the way (a configuration
   synchronization, as after the upgrade in Lab 3.3).

**Track 1 — fault 2, LLDP filtered:**

5. **C2 and C3 with `vmbrFL`:** clear the LLDP bit on the bridge, as in Lab 2.3's
   negative test:

   ```bash
   # on proxmox-1
   echo 0 > /sys/class/net/vmbrFL/bridge/group_fwd_mask
   ```

   **C1, and C2 or C3 with passthrough:** stop the FortiLink interface from
   receiving LLDP (C1: `<FL_PORT>`; C3: `port4`):

   ```text
   FGT # config system interface
   edit port3
   set lldp-reception disable
   next
   end
   ```

6. Wait at least five minutes (longer than an LLDP neighbor's hold time; the
   local documents do not give the switch's value), then look again:

   ```text
   FGT # diagnose switch-controller switch-info lldp neighbors-summary <SWITCH_SN>
   FGT # execute switch-controller get-conn-status
   FGT # execute switch-controller get-physical-conn standard port3
   ```

   Predict which view changes. **Answer:** the documentation does not say
   whether an authorized session needs LLDP after discovery, so record it. The
   LLDP view is the one to watch: with the bridge mask cleared, the switch's
   LLDP frames no longer reach the FortiGate; with `lldp-reception disable`,
   they reach it and are ignored. Note whether `get-conn-status` stays
   `Authorized/Up` (the management session is IP traffic, which the bridge
   still forwards) and whether `get-physical-conn` still draws the link.

7. Revert, and confirm that the LLDP neighbor returns:

   ```bash
   # on proxmox-1 (vmbrFL)
   echo 16384 > /sys/class/net/vmbrFL/bridge/group_fwd_mask
   ```

   ```text
   FGT # config system interface
   edit port3
   set lldp-reception enable
   next
   end
   ```

**Track 1 — fault 3, neighbor detection changed:**

8. Switch the FortiLink interface to FortiLink-protocol detection, wait five
   minutes, and look at both views; then return it to `lldp`:

   ```text
   FGT # config system interface
   edit port3
   set fortilink-neighbor-detect fortilink
   next
   end
   FGT # execute switch-controller get-conn-status
   FGT # execute switch-controller get-physical-conn standard port3
   FGT # config system interface
   edit port3
   set fortilink-neighbor-detect lldp
   next
   end
   ```

   Predict the effect on the managed switch. **Answer:** none documented.
   The setting chooses how FortiOS **detects** FortiSwitch neighbors (FortiLink
   Guide, p. 24), and Chapter 02 even uses the change as a repair step, so a
   switch that is already managed may not notice; record what you see. The
   mismatch matters for discovery: a reset switch on a path that drops one
   kind of frame is found only by the method whose frames get through.

**Track 1 — fault 4, the switch deauthorized:**

9. Deauthorize the switch and watch both sides for three minutes:

   ```text
   FGT # config switch-controller managed-switch
   edit <SWITCH_SN>
   set fsw-wan1-admin disable
   next
   end
   FGT # execute switch-controller get-conn-status
   FSW # execute switch-controller get-conn-status
   ```

   Predict the STATUS. **Answer:** not documented for a switch that was
   authorized and then deauthorized. The guide shows `Discovered/Down` with
   VERSION and ADDRESS `N/A` only for switches never authorized (p. 52); record
   the STATUS you see, and whether the switch rebooted or returned to factory
   defaults (watch the console). If step 2 showed `switch-on-deauth
   factory-reset`, expect a reset.

10. Authorize it again and check that its configuration returned:

    ```text
    FGT # config switch-controller managed-switch
    edit <SWITCH_SN>
    set fsw-wan1-admin enable
    next
    end
    FGT # execute switch-controller get-conn-status
    FGT # execute switch-controller get-sync-status all
    FSW # diagnose switch physical-ports summary port1
    ```

    When the row is `Authorized/Up` again, `port1` shows native VLAN 1741, and
    `get-sync-status` matches the baseline, the entry's configuration has been
    pushed back, as in the Chapter 11 round trip. If the switch was reset and
    asks for a password at the console, the profile `fsw-174-prof` sets your
    recorded password once it is managed.

**Track 1 — fault 7, an inter-switch link member (S3):**

11. Unplug `port24` on `FSW-A` (one of the two ICL members to `FSW-B`), wait a
    minute, and read the ICL and the trunks; then plug it back in:

    ```text
    FGT # diagnose switch-controller switch-info mclag icl
    FGT # execute switch-controller get-conn-status
    FSW # diagnose switch mclag icl
    FSW # diagnose switch trunk summary
    ```

    Predict whether `FSW-B` stays managed. **Answer:** yes: `port23` still
    joins the switches, which is why Fortinet recommends at least two ICL links
    (FortiLink Guide, p. 89). The ICL trunk shows one member down; record how
    the controller's `mclag icl` output shows it. After you plug `port24` back
    in, both members are up again.

**Track 2: read-and-predict.** First run the baseline commands of step 2 that
need no switch (`get-conn-status`, `get-physical-conn standard port3`,
`get-sync-status all`, `get switch-controller global`) on your controller and
record them. Then predict each signature:

1. Fault 1, the cable. Predict the row of a managed switch whose FortiLink cable
   was pulled a minute ago. **Answer:** `Authorized/Down`, ADDRESS `0.0.0.0`,
   VERSION as last known; in the topology, a dashed line and a broken-link icon
   (pp. 323, 348).
2. Fault 5, the wrong VDOM. An administrator runs `get-conn-status` in VDOM
   `root` and sees no switches, although the switch is healthy. The guide's
   example header reads `Managed-devices in current vdom vdom1:` with
   `FortiLink interface : port11` (p. 52). Predict the cause. **Answer:** the
   table is per VDOM, and the FortiLink interface (with its switches) belongs to
   another VDOM; run the command in that VDOM. On C2 the evaluation's single
   traffic VDOM (Chapter 10) makes this fault impossible to build.
3. Fault 6, incompatible firmware. A switch moved to a FortiSwitchOS build
   that the FortiLink Compatibility table does not list for the controller's
   FortiOS build stays `Authorized/Down`, and the topology shows the link
   broken. Predict the documented reason and the fix. **Answer:** firmware
   versions out of step (p. 323): check the compatibility table (p. 12), then
   load a supported build on the switch from its console (Lab 2.4's TFTP
   procedure), because the controller cannot push firmware to a switch it
   cannot manage.
4. A never-authorized switch: `S248EPTF18001827 N/A Discovered/Down 2 N/A`
   (p. 52). Predict the one change that manages it. **Answer:** `set
   fsw-wan1-admin enable` on its entry (Chapter 03).
5. A row shows `Authorized/Up` with FLAG `E`. Predict the meaning and the next
   two commands. **Answer:** configuration sync error; `execute
   switch-controller get-sync-status all`, then `diagnose switch-controller
   trigger config-sync <switch>` (pp. 319, 343).
6. Fault 2 on Track 2's own path. On C2 with `vmbrFL`, the bridge's
   `group_fwd_mask` is 0 and a factory-reset switch is cabled. Predict
   `get-conn-status` after ten minutes with `fortilink-neighbor-detect lldp`.
   **Answer:** no row for the switch: the bridge drops LLDP, so the controller
   never discovers it (Chapter 02); switching detection to `fortilink` is
   Chapter 02's diagnostic step.

**Expected result:** Track 1: each induced fault left a recorded signature in
`get-conn-status`, the LLDP view, or the topology view, and each was reverted;
the switch (and `FSW-B` on S3) is `Authorized/Up` again with `get-sync-status`
matching the baseline; the existence and value of `switch-on-deauth` and the
deauthorized STATUS are recorded. Track 2: the baseline output and the six
predictions are recorded.

**Negative test:** Ask for a synchronization of a switch the controller does
not manage, using the documented serial of a switch that is not yours:

```text
FGT # diagnose switch-controller trigger config-sync S124EN5918003682
```

The command fails or does nothing, and no row changes in `get-conn-status`;
record the message. The same works on Track 2.

**Rollback:** Every fault was reverted in its own step. If the switch does not
return, check in reverse order: `fsw-wan1-admin enable`,
`fortilink-neighbor-detect lldp`, `lldp-reception enable` or
`group_fwd_mask 16384`, and the cable; then restore `fgt-pre-12-4-174.conf` if
the entry itself was damaged.

**Lab verified by:** *pending*

### Lab 12.5 — Harden the managed switch and collect the evidence

**Objective:** Apply the hardening that FortiLink mode allows against the
Volume CLXXII FortiSwitch prerequisites and Lab 8.5 Part D's Layer 2 rules,
record the rows that FortiLink mode cannot meet, and collect one piece of
evidence per row.

**Platform notes:** Hands-on on C1, C2, and C3 with S1, S2, or S3 (on S3, apply
the per-port steps to `FSW-A`; `FSW-B` takes the global objects automatically).
The sFlow row is evidence on S2 and S3 and an exception on S1. IP source guard
(`CISC-L2-000140`) is an S3-only row and stays an exception in this lab, as in
Lab 8.5. No policy is added; on C2 the three slots stay P1, P2, and
`P3-snmp-174`. Track 2: build the controller side only, and on the stand-in
entry only if Lab 2.2's third outcome applies.

**Track 1, Part A — administration and management access (P1, P10):**

1. Back up the controller:

   ```text
   FGT # execute backup config tftp fgt-pre-12-5-174.conf 10.30.99.50
   ```

2. Read the switch profile and add a configuration revision at every logout
   (FortiLink Guide 7.6.7, p. 352):

   ```text
   FGT # config switch-controller switch-profile
   edit "fsw-174-prof"
   set revision-backup-on-logout enable
   next
   end
   FGT # show switch-controller switch-profile fsw-174-prof
   ```

   Evidence for P1: `login-passwd-override enable`, a password, `login enable`,
   and both revision backups. Remote administrator authentication itself is an
   **exception**: the feature matrix marks RADIUS and TACACS+ for
   administrative authentication as standalone only in both columns. Console
   login stays enabled as the recovery path; record that decision.

3. Check the management access the switch received from `la-174` (Lab 12.2) and
   the management VLAN:

   ```text
   FGT # show switch-controller security-policy local-access la-174
   FGT # get system interface port3
   FSW # show system interface internal
   FSW # diagnose switch vlan list 4094
   ```

   Evidence for P10: no `http` or `telnet` in the switch's `allowaccess`
   lines, and `switch-controller-mgmt-vlan` 4094 on the FortiLink interface
   with the switch's internal interface in VLAN 4094, a VLAN no user port is
   in. Record the lines exactly; the guide shows the policy but not how the
   switch prints the result.

**Track 1, Part B — logging (P4, P7):**

4. Send the switch's logs to `ubuntu-ws` as well as to the FortiGate. `syslogd`
   is a valid name in both the guide (p. 292) and the FortiOS 7.6.0 reference:

   ```text
   FGT # config switch-controller remote-log
   edit "syslogd"
   set status enable
   set server "10.200.0.20"
   set port 514
   set severity information
   set csv disable
   set facility local7
   next
   end
   FGT # show switch-controller switch-log
   ```

5. Log out of the switch console and log in again to cause log events, then
   look on `ubuntu-ws`:

   ```bash
   # ubuntu-ws
   ~/watch-174.sh
   grep '<SWITCH_SN>' /var/log/syslog | tail -5
   ```

   Evidence for P4 and P7: UDP 514 datagrams from `10.255.1.2` and lines that
   name the switch's serial (its factory host name). `switch-log` shows export
   to the FortiGate enabled (the default). Reliable (TCP or TLS) syslog is an
   **exception**: the matrix marks it standalone only.

**Track 1, Part C — time (P5):**

6. Record the FortiGate's NTP settings and the FortiLink DHCP server, then let
   the FortiGate serve NTP on the FortiLink interface (FortiLink Guide, p. 25).
   `append` keeps any interfaces already listed:

   ```text
   FGT # show system ntp
   FGT # show system dhcp server <FL_DHCP_ID>
   FGT # config system ntp
   set server-mode enable
   append interface "port3"
   end
   ```

   If the FortiLink DHCP server does not already hand out the FortiGate as NTP
   server (`ntp-service local`, the form Chapter 02 used), set it:

   ```text
   FGT # config system dhcp server
   edit <FL_DHCP_ID>
   set ntp-service local
   next
   end
   ```

7. Read the switch's view after its next DHCP renewal (or after fault 1 of Lab
   12.4, if you repeat it):

   ```text
   FSW # diagnose sys ntp status
   ```

   The guide says a switch's NTP server can be "provided by DHCP" (p. 65, in
   the Layer 3 FortiLink context) but does not say how a managed switch on a
   Layer 2 FortiLink picks its server, and the FortiGate can serve time only if
   its own clock is synchronized. Record `synchronized`, the server, and the
   stratum. Authenticated NTP between the switch and the FortiGate (P5 asks for
   keys) is not documented for managed switches: record it as an
   **exception**.

**Track 1, Part D — SNMP (P6):**

8. Remove the v2c community that Lab 12.2 used for the trap test, then poll
   with SNMPv3 again (Lab 12.2 step 7):

   ```text
   FGT # config switch-controller snmp-community
   delete 1
   end
   FGT # show switch-controller snmp-community
   FGT # show switch-controller snmp-user
   ```

   Evidence for P6: no community, user `snmp-174` with `security-level
   auth-priv`, `auth-proto sha256`, and a privacy protocol, and a working
   `snmpwalk -v3`. The Volume CLXXII row asks for AES-256: if `snmpwalk` on
   `ubuntu-ws` lists AES-256 among its `-x` choices, set `priv-proto aes256`
   on the controller, poll with the matching `-x` value, and record it;
   otherwise record AES-128 as a lab deviation.

**Track 1, Part E — Layer 2 hygiene (P12, P13, and Lab 8.5 Part D):**

9. Turn DHCP snooping and then DAI on for `fsw-users` (DHCP snooping first, P12;
   Chapter 08's forms):

   ```text
   FGT # config system interface
   edit "fsw-users"
   set switch-controller-dhcp-snooping enable
   next
   end
   FGT # config system interface
   edit "fsw-users"
   set switch-controller-arp-inspection enable
   next
   end
   ```

   Renew endpoint A's lease and ping its gateway; then read the switch's
   database:

   ```bash
   # endpoint A
   sudo dhclient -r <IFACE> && sudo dhclient <IFACE>
   ping -c 3 10.174.41.1
   ```

   ```text
   FSW # get switch dhcp-snooping database-summary
   FSW # get switch dhcp-snooping client-db-details
   ```

   If endpoint A uses another DHCP client than `dhclient`, renew it the way
   Chapter 08 did.

10. Block unknown unicast flooding to the host ports (`CISC-L2-000120`, the
    form Lab 8.5 Part D planned: unknown unicast only, `rate 0`, which the
    FortiOS 7.6.0 reference defines as "drop all"), mark the unused `port4`
    down (`CISC-L2-000210`), and refuse tagged frames on endpoint B's port
    (`CISC-L2-000250`):

    ```text
    FGT # config switch-controller storm-control-policy
    edit "storm-uu-174"
    set description "Lab 12.5 unknown unicast"
    set storm-control-mode override
    set rate 0
    set broadcast disable
    set unknown-unicast enable
    set unknown-multicast disable
    next
    end
    FGT # config switch-controller managed-switch
    edit <SWITCH_SN>
    config ports
    edit "port1"
    set storm-control-policy "storm-uu-174"
    next
    edit "port2"
    set storm-control-policy "storm-uu-174"
    set discard-mode all-tagged
    next
    edit "port4"
    set description "unused-174"
    set status down
    next
    end
    next
    end
    ```

    `port1` keeps `discard-mode none`, because its allowed list carries tagged
    VLANs by design (Chapter 04); record that as an exception for
    `CISC-L2-000250`. Check that both endpoints still reach their gateways, then
    read the ports on the switch:

    ```text
    FSW # diagnose switch physical-ports summary port2
    FSW # diagnose switch physical-ports summary port4
    ```

**Track 1, Part F — flow collection and image integrity (P18, P9):**

11. Evidence for P18 (S2, S3): `show switch-controller sflow` and the UDP 6343
    section of `~/watch-174.sh` from Lab 12.2. On S1, record the exception (no
    sFlow on the FS-108F).

12. Check the image the switch runs and the one on its other partition, and the
    images the controller still holds:

    ```text
    FSW # get system status
    FSW # diagnose sys firmware info
    FSW # execute verify image primary
    FSW # execute verify image secondary
    FSW # diagnose sys flash list
    FGT # execute switch-controller switch-software list-available
    ```

    Evidence for image integrity (Volume CLXXII, OS image signature
    verification row): `Firmware Signature` not `invalid`, `BIOS Signature` and
    `Firmware Signature` valid in `diagnose sys firmware info`, and "No issue
    found!" for the primary image (the CLI Reference's example wording, p. 464).
    A model without a secondary partition may refuse the second command; record
    it. Check your exact model against note 17 (FS-224D-FPOE and FS-248D have
    no image signature verification).

**Track 1, Part G — the evidence table:**

13. Fill in the last column from Parts A to F. The SRG IDs are those of the
    Volume CLXXII, Chapter 11 rows, and the rules those of Lab 8.5 Part D:

    | Row | Requirement | FortiLink-mode setting in this lab | Your evidence |
    | --- | --- | --- | --- |
    | P1 (`SRG-APP-000516-NDM-000336`) | Remote administrator authentication | Exception (standalone only); compensating: profile password override, console login control | |
    | P4, P7 (`SRG-APP-000516-NDM-000350`, `SRG-APP-000515-NDM-000325`) | Logs off-loaded to a central server | `remote-log` `syslogd` to `10.200.0.20`; `switch-log` to the FortiGate; reliable syslog an exception | |
    | P5 (`SRG-APP-000920-NDM-000320`) | Synchronized, authenticated time | FortiGate NTP server on the FortiLink interface; authentication an exception | |
    | P6 (`SRG-APP-000395-NDM-000310`) | SNMPv3 with SHA-2 and AES | `snmp-174`, `auth-priv`, `sha256`, AES; no community | |
    | P10 | Management on its own VLAN, limited protocols | FortiLink management VLAN 4094; `la-174` without HTTP and Telnet | |
    | P12, `CISC-L2-000130`, `CISC-L2-000150` | DHCP snooping, then DAI, on user VLANs | `fsw-users` snooping and ARP inspection | |
    | `CISC-L2-000120` | Unknown unicast flooding blocked on host ports | `storm-uu-174` on `port1` and `port2` | |
    | `CISC-L2-000210` | Unused ports disabled | `port4` `status down`, `unused-174` | |
    | P13, `CISC-L2-000220`, `CISC-L2-000270` | No default or native VLAN 1 on host ports | `port1` native `fsw-users`, `port2` native `fsw-iot` (since Chapter 04) | |
    | `CISC-L2-000250` | Host ports as access ports | `port2` `discard-mode all-tagged`; `port1` an exception | |
    | `CISC-L2-000140` | IP source guard on host ports | Exception in this lab (S3 only; Lab 8.2) | |
    | P18 (`SRG-APP-000516-NDM-000350`) | Flow collection | sFlow to `ubuntu-ws` (S2, S3); exception on S1 | |
    | P9 (`SRG-APP-000131-NDM-000243`) | Signed, verified images | Signature checks and `verify image` | |

**Track 2:** Do steps 1, 2, 4, 6, 8, and 9 (the controller blocks) and step 10's
storm-control policy on your controller, and check each with its `show`
command. If Lab 2.2's third outcome applies, also apply step 10's port settings
to `S248EPTF18000000`. Fill in the evidence table with the controller-side
evidence and mark every switch-side cell "Track 2: not observable".

**Track 2: read-and-predict.**

1. An auditor asks for the managed switch's TACACS+ configuration. Predict your
   answer. **Answer:** there is none to show: the 7.6.7 feature matrix marks
   TACACS+ (and RADIUS) for administrative authentication as standalone only;
   in FortiLink mode the controller sets the switch's admin password through
   the switch profile, and that is the evidence offered.
2. Predict what happens to a FortiSwitch admin password that a profile pushed,
   if the profile's override is turned off. **Answer:** the old password stays
   on the switch, unless a profile with the override enabled and no password
   is applied (FortiLink Guide, p. 43).
3. `diagnose sys firmware info` on an FS-148E prints `BIOS Signature: valid` and
   `Firmware Signature: invalid` (the CLI Reference's example, p. 389). Predict
   the finding. **Answer:** the switch runs an image that did not pass signature
   verification, such as an interim build; load a GA image and check again, as
   Lab 2.4 did.

**Expected result:** Track 1: the profile has both revision backups; the switch
shows no HTTP or Telnet access and its management in VLAN 4094; switch logs
reach `ubuntu-ws`; the switch's NTP state is recorded; the v2c community is
gone and SNMPv3 still answers; snooping and DAI run on `fsw-users` without
breaking endpoint A; `port1` and `port2` carry the unknown-unicast policy,
`port2` discards tagged frames, `port4` is down; the image checks pass; and
every row of the evidence table is filled in, the exceptions included. Track 2:
the controller objects exist and the table holds the controller-side evidence.

**Negative test:** Poll with the deleted community:

```bash
# ubuntu-ws
snmpwalk -v2c -c trap-174 10.255.1.2 1.3.6.1.2.1.1
```

It times out: the community no longer exists, and it never allowed queries.
Then send a tagged frame from endpoint B: create a VLAN subinterface for VLAN
1743 and ping the gateway through it (`ip-link(8)`):

```bash
# endpoint B
sudo ip link add link <IFACE_B> name <IFACE_B>.1743 type vlan id 1743
sudo ip addr add 10.174.43.21/24 dev <IFACE_B>.1743
ping -c 3 -I <IFACE_B>.1743 10.174.43.1
sudo ip link del <IFACE_B>.1743
```

The ping fails, because `port2` discards tagged frames, while the untagged
ping from `10.174.43.20` keeps working. Track 2: show that
`show switch-controller snmp-community` is empty.

**Rollback:** Keep the hardened state; Lab 12.6 removes it with the rest of the
lab. To undo only this lab, restore `fgt-pre-12-5-174.conf`.

**Lab verified by:** *pending*

### Lab 12.6 — Tear down the lab

**Objective:** Archive the final state, retire every switch to factory
defaults, return every controller to its pre-volume configuration, undo the
Proxmox, Nexus, and VM changes of Chapter 02, clean the hosts, and confirm the
result with the final checklist.

**Platform notes:** Hands-on on every option. Part B is Track 1 only (on S3 it
retires `FSW-B` first). Part C differs per controller: C2 returns `port3` to
VLAN 202 with the file `fgt1-pre-174.conf`, C3 removes `port4` with
`fgt-c3-pre-174.conf`, and C1 returns to `c1-fgt-base-174.conf` (or is reset
and retired). Part D applies to C2 and C3 (Option A or B); Part E to every
option that used the Nexus (Lab 2.4's switch port, and C1's two ports). Track 2
does Parts A, C, D (C2: `net2` back to VLAN 202 with its link up), and F.
Allow two to three hours.

**Track 1, Part A — archive:**

1. Back up the controller's final state, and record what Part C must remove:

   ```text
   FGT # execute backup config tftp fgt-final-174.conf 10.30.99.50
   FGT # execute switch-controller get-conn-status
   FGT # show switch-controller global
   FGT # show system csf
   FGT # show firewall policy
   FGT # execute switch-controller switch-software list-available
   ```

2. Capture the switch's last managed configuration on the console host (on S3,
   repeat for `FSW-B` with its own file name):

   ```bash
   picocom -b 9600 --logfile fsw-final-174.txt /dev/ttyUSB0
   ```

   ```text
   FSW # show
   ```

**Track 1, Part B — retire the switches:**

3. **S3 only:** retire `FSW-B` first, while `FSW-A` still carries its path to the
   controller (Lab 3.5's command; FortiLink Guide 7.6.7, p. 322):

   ```text
   FGT # execute switch-controller switch-action set-standalone <FSWB_SN>
   ```

   When `FSW-B`'s console shows the factory login, unplug the ICL cables
   (`FSW-A` `port23` and `port24`).

4. Retire `FSW-A` (S1, S2: the only switch):

   ```text
   FGT # execute switch-controller switch-action set-standalone <SWITCH_SN>
   ```

   When the switch's console shows the factory login, unplug the FortiLink
   cable from `<FSW_FL_PORT>` and both endpoint cables.

5. Deauthorize and delete every entry (Track 2: the stand-in entry), then
   check the discovery list and the Security Fabric trusted list. Remove any
   serial of yours that `set-standalone` added to `disable-discovery` (the
   `unselect` form of Lab 3.5) and any `deny` entry for it in the trusted list:

   ```text
   FGT # config switch-controller managed-switch
   edit <SWITCH_SN>
   set fsw-wan1-admin disable
   next
   end
   FGT # config switch-controller managed-switch
   delete <SWITCH_SN>
   end
   FGT # config switch-controller managed-switch
   delete <FSWB_SN>
   end
   FGT # config switch-controller managed-switch
   delete S248EPTF18000000
   end
   FGT # show switch-controller global
   FGT # config switch-controller global
   unselect disable-discovery <SWITCH_SN>
   end
   FGT # show system csf
   ```

   Run each `delete` only for entries you have (`<FSWB_SN>` on S3,
   `S248EPTF18000000` on Track 2), and `unselect` only for serials the list
   shows. If `show system csf` lists one of your serials under `config
   trusted-list` with `action deny`, remove it with `delete <SERIAL>` inside
   `config system csf`, `config trusted-list`; the guide shows the list
   (p. 321) but not its removal, so record what FortiOS accepts. The pre-volume
   comparison in Part C catches anything left.

6. On each switch console, log in (factory defaults: `admin`, no password; set a
   temporary password when prompted), confirm that it is standalone and on the
   expected build, and reset it one last time so that it leaves the lab at
   factory defaults with no password of yours:

   ```text
   FSW # get system status
   FSW # execute switch-controller get-conn-status
   FSW # execute factoryreset
   ```

   Power the switch off at the login prompt. If it changes owner, release or
   transfer its FortiCare registration in the support portal (Chapter 02); this
   volume never changed it.

**Track 1, Part C — return the controller (C2 and C3; C1 in step 15):**

7. Remove this chapter's monitoring and hardening objects. The entries that
   used `la-174` and `storm-uu-174` are gone, so the objects are free. Use the
   values recorded in Lab 12.2 step 3 and Lab 12.5 step 6 where a setting
   returns rather than disappears:

   ```text
   FGT # config firewall policy
   delete <P3_ID>
   end
   FGT # config switch-controller flow-tracking
   config collectors
   delete "ws-174"
   end
   end
   FGT # config switch-controller sflow
   set collector-ip 0.0.0.0
   end
   FGT # config switch-controller snmp-user
   delete "snmp-174"
   end
   FGT # config switch-controller snmp-sysinfo
   set status disable
   end
   FGT # config switch-controller remote-log
   edit "syslogd"
   set status disable
   next
   end
   FGT # config switch-controller security-policy local-access
   delete "la-174"
   end
   FGT # config switch-controller storm-control-policy
   delete "storm-uu-174"
   end
   FGT # config system ntp
   unselect interface "port3"
   end
   ```

   Set `snmp-sysinfo` status and NTP `server-mode` to the values you recorded
   (the block shows `disable` for sysinfo, the FortiOS 7.6.0 default); if
   `remote-log` had no `syslogd` entry before Lab 12.5, `delete "syslogd"`
   instead of disabling it.

8. Remove the switch-controller objects of Chapters 03–07, and the uploaded
   images. The delete command is in the FortiOS 8.0.1 CLI Reference, not in the
   FortiLink Guide 7.6.7, so type `?` after `switch-software` first:

   ```text
   FGT # config switch-controller security-policy 802-1X
   delete "dot1x-174-port"
   delete "mab-174"
   end
   FGT # config user group
   delete "dot1x-174"
   end
   FGT # config switch-controller switch-profile
   delete "fsw-174-prof"
   end
   FGT # config switch-controller stp-instance
   delete "1"
   end
   FGT # config switch-controller stp-settings
   set name <ORIG_STP_NAME>
   set revision <ORIG_STP_REVISION>
   end
   FGT # execute switch-controller switch-software delete <IMAGE_NAME>
   ```

   `<ORIG_STP_NAME>` and `<ORIG_STP_REVISION>` are the values Lab 5.1 step 1
   recorded (in the pre-volume file if you did not record them).

9. Remove the policies and the objects they named. **C2 and C3:** delete P2 and
   take `FSW-LAN` (and `fsw-lan-174`, if Lab 4.1 appended it) out of P1, so that
   P1 is as Lab 4.1 step 1 recorded it. **C1:** delete P2 and
   `P1-fsw-lan-internet`:

   ```text
   FGT # config firewall policy
   delete <P2_ID>
   end
   FGT # config firewall policy
   edit <P1_ID>
   unselect srcintf "FSW-LAN"
   unselect srcaddr "fsw-lan-174"
   next
   end
   FGT # config firewall address
   delete "radius-174"
   delete "ubuntu-ws"
   delete "fsw-lan-174"
   end
   FGT # config firewall service custom
   delete "lab-svc-174"
   end
   FGT # config user radius
   delete "radius-174"
   end
   ```

   On C1, `delete <P1_ID>` replaces the `edit <P1_ID>` block.

10. Remove the lab VLANs in Lab 4.1's rollback order: the DHCP server, the zone,
    then the five interfaces (skip what C2's Lab 4.1 NO-GO never created):

    ```text
    FGT # config system dhcp server
    delete <USERS_DHCP_ID>
    end
    FGT # config system zone
    delete "FSW-LAN"
    end
    FGT # config system interface
    delete "fsw-users"
    delete "fsw-voice"
    delete "fsw-iot"
    delete "fsw-guest"
    delete "fsw-tenant"
    end
    ```

11. Release the FortiLink interface. List what still refers to it, delete the
    auto-created VLAN interfaces and their DHCP servers from the `show` output
    (their names follow the templates: `quarantine`, `rspan`, `voice`,
    `video`, `onboarding`, and the NAC segment), then turn FortiLink off and
    delete its DHCP server:

    ```text
    FGT # diagnose sys cmdb refcnt show system.interface.name port3
    FGT # show system dhcp server
    FGT # config system interface
    edit port3
    set fortilink disable
    next
    end
    FGT # config system dhcp server
    delete <FL_DHCP_ID>
    end
    ```

    The documentation does not say whether FortiOS lets you delete the
    auto-created VLANs while FortiLink is enabled, or removes them when it is
    disabled. Delete each with `delete "<name>"` under `config system interface`
    (and its DHCP server by ID) before or after `set fortilink disable`,
    whichever FortiOS accepts, and record which. If FortiLink cannot be disabled,
    the guide's advice is to disable it first and retry the deletions (p. 33).

12. Give the port back its pre-volume role. **C2:** set `port3` back to the
    `show system interface port3` output that Lab 2.1 step 3 recorded (alias,
    address, access, VLAN 202 role), and re-create the VLAN 202 DHCP server and
    policies from the same records; with the restore path of step 14 you skip
    this step. **C3:** clear `port4` (`unset alias`, `unset ip`,
    `unset allowaccess` under `config system interface`, `edit port4`); Part D
    removes the vNIC. Return `switch-controller` under `config system global`
    to its pre-volume value if Lab 2.2 changed it.

13. Back up the result and compare it with the pre-volume file. On VM 140, or on
    any Linux host that holds both files, drop the header lines and the lines
    with encrypted secrets (`ENC`), which can differ between two backups of the
    same secret, and compare (C3: `fgt-c3-pre-174.conf`):

    ```text
    FGT # execute backup config tftp fgt-teardown-174.conf 10.30.99.50
    ```

    ```bash
    # on VM 140 (in /tftpboot) or another Linux host
    grep -v -e '^#' -e ' ENC ' fgt1-pre-174.conf > pre.txt
    grep -v -e '^#' -e ' ENC ' fgt-teardown-174.conf > post.txt
    diff pre.txt post.txt
    ```

    Expected differences are the ones the volume did not cause (for example
    `uuid` lines of objects you re-created by hand in step 12, or changes made
    outside the lab since Chapter 02). Any remaining `switch-controller`,
    `fsw-`, `174`, or FortiLink line is a leftover: remove it, or take step 14.

14. **Fallback:** restore the pre-volume file. The controller reboots with the
    configuration it had before Chapter 02 touched it (C2: VLAN 202 on `port3`,
    its policies and DHCP server; C3: no `port4` settings). Everything changed on
    the controller since that backup is lost, lab or not:

    ```text
    FGT # execute restore config tftp fgt1-pre-174.conf 10.30.99.50
    ```

    C3: `execute restore config tftp fgt-c3-pre-174.conf 10.30.99.50`. There is
    no `fgt-pre-2-*` file: these Chapter 02 files are the earliest backups.

15. **C1:** if the FortiGate stays in your lab, restore `c1-fgt-base-174.conf`
    the same way (it holds the factory `fortilink` interface's original
    settings and `<FL_PORT>` in its hardware switch); to return `<FL_PORT>` by
    hand instead, add it back to `lan` under `config system virtual-switch`,
    `edit lan`, `config port`, `edit <FL_PORT>`. If you are retiring the unit,
    reset it (`execute factoryreset`, as in Lab 2.1), unplug it, and do Part E
    for its two Nexus ports.

**Track 1, Part D — return the hypervisor (C2 and C3):**

16. Return the FortiLink vNIC, or replace the passed-through NIC with the
    original vNIC. Use the model and MAC that Lab 2.1 recorded (`qm(1)`):

    ```bash
    # on proxmox-1
    qm config 120 | grep -e ^net -e ^hostpci
    # C2, Option A (vmbrFL): port3 back on VLAN 202, link up
    qm set 120 --net2 <MODEL>=<PORT3_MAC>,bridge=vmbr2,tag=202
    # C2, Option B (passthrough): needs the VM stopped
    qm shutdown 120
    qm set 120 --delete hostpci0
    qm set 120 --net2 <MODEL>=<PORT3_MAC>,bridge=vmbr2,tag=202
    qm start 120
    # C3, Option A: remove port4
    qm shutdown 120
    qm set 120 --delete net3
    qm start 120
    # C3, Option B: qm shutdown 120; qm set 120 --delete hostpci0; qm start 120
    qm config 120 | grep -e ^net -e ^hostpci
    ```

    Run only the lines for your option. On Track 2 (C2), `net2` is still on
    `vmbr2` with `tag=202,link_down=1` from Lab 2.1; the first `qm set` line,
    without `link_down`, brings it up.

17. Remove the bridge and the helper script. Delete the `auto <NEW_NIC>`,
    `iface <NEW_NIC>`, `auto vmbrFL`, and `iface vmbrFL` stanzas from
    `/etc/network/interfaces` (Lab 2.3), then:

    ```bash
    # on proxmox-1
    ifreload -a
    ip -br link | grep -i vmbrfl
    rm /root/fl-path-check.sh
    ```

    The `grep` prints nothing when the bridge is gone. Remove `tcpdump`
    (`apt remove tcpdump`) only if you installed it for Chapter 02.

18. **Option B only:** if no other VM on proxmox-1 uses PCI passthrough, remove
    the vfio module list that Lab 2.3 added and rebuild the initramfs; the change
    takes effect at the next host reboot. Leave VT-d in the BIOS as your site
    prefers:

    ```bash
    # on proxmox-1
    grep -l hostpci /etc/pve/qemu-server/*.conf
    rm /etc/modules-load.d/vfio.conf
    update-initramfs -u -k all
    ```

    Run the last two lines only if the `grep` lists no VM.

19. Retire `radius-174` (VM 174). Back it up first if you may want it again,
    then destroy it; `--purge 1` also removes it from backup jobs and
    replication (`qm(1)`). Destroying a VM is permanent:

    ```bash
    # on proxmox-1
    qm shutdown 174
    vzdump 174 --storage <BACKUP_STORAGE> --mode stop
    qm destroy 174 --purge 1
    ```

    Skip `vzdump` if you do not want a copy; skip `qm destroy` to keep the VM
    stopped instead. Unplug the dedicated NIC's cable; removing the card
    itself needs a host shutdown and is optional.

**Track 1, Part E — return the Nexus ports:**

20. The Nexus port that Lab 2.4 and Chapter 11 used for the switch's management
    is already shut. Return it to the unused state (the Nexus default is
    `switchport shutdown`, Chapter 02), and do the same for C1's two ports if C1
    is retired:

    ```text
    configure terminal
    interface Ethernet1/<free>
      no description
      no switchport access vlan
      no spanning-tree port type
      shutdown
    end
    copy running-config startup-config
    show running-config interface Ethernet1/<free>
    ```

    Compare the last command's output with the port's entry in
    [Volume CM, Chapter 04](../../volume-900-tims-lab-gear/chapters/04-current-device-configurations.md)
    from before the volume.

**Track 1, Part F — the services and the hosts:**

21. On `ubuntu-ws`, remove the syslog listener, the trap configuration line,
    the watcher, and the packages Lab 12.2 installed:

    ```bash
    # ubuntu-ws
    sudo rm /etc/rsyslog.d/10-fsw-174.conf
    sudo systemctl restart rsyslog
    sudo sed -i '/^authCommunity log trap-174$/d' /etc/snmp/snmptrapd.conf
    rm ~/watch-174.sh
    sudo apt remove -y snmp snmptrapd
    ```

    Keep any package that `ubuntu-ws` had before the volume (for example
    `tcpdump`).

22. On the endpoints, remove what the volume added (Labs 2.5, 4.2, 7.2, 8.1,
    10.2), package removals only for packages you installed for the volume:

    ```bash
    # endpoint A
    sudo rm /etc/wpa_supplicant/wired-174.conf
    sudo apt remove -y iputils-arping
    # endpoint B
    sudo ip addr del 10.174.43.20/24 dev <IFACE_B>
    sudo apt remove -y dnsmasq iperf
    ```

    Remove `wpasupplicant` and `tcpdump` too if the endpoints did not have them
    before Chapter 02.

23. On VM 140 and the console host, decide what to keep. Keep the pre-volume
    files (`c1-fgt-base-174.conf`, `fgt1-pre-174.conf`, `fgt-c3-pre-174.conf`)
    and `fgt-final-174.conf` until you are sure; the chapter backups
    (`fgt-pre-3-3-174.conf` to `fgt-pre-12-5-174.conf`, `fgt-post-11-174.conf`,
    `fgt-teardown-174.conf`), the standalone backup `fsw-sa-11-174.conf`, the
    console captures (`fsw-managed-pre-11-174.txt`,
    `fsw-managed-post-11-174.txt`, `fsw-final-174.txt`), and the firmware images
    in `/tftpboot` can go. They contain lab secrets in encrypted form.

**Track 1, Part G — final checks:**

24. Check the controller and the network:

    ```text
    FGT # execute switch-controller get-conn-status
    FGT # get system interface physical
    FGT # show firewall policy
    FGT # execute ping <TEST202_IP>
    ```

    Predict each. **Answer:** no switch rows; on C2, three physical interfaces
    with `port3` back in its VLAN 202 role, on C3 three again (no `port4`); the
    policies of the pre-volume file; and on C2 the ping to the VLAN 202 test VM
    succeeds, the reverse of Lab 2.1's negative test.

**Track 2:** Do step 1 (without the switch-image line if you uploaded none),
step 5's stand-in deletion, steps 7–14 for the objects you built (on FGT-1
alone: the C2 steps), step 16's first `qm set` line (C2), step 19, and steps 21
and 23. Track 2 never used the Nexus, the endpoints, or `vmbrFL` unless you
built them anyway.

**Track 2: read-and-predict.**

1. An administrator retires a switch with `execute switch-controller
   factory-reset <switch-id>`, deletes its entry, and leaves it cabled to a
   FortiLink interface with automatic authorization enabled. Predict the next
   day. **Answer:** the switch is managed again: a factory-reset switch looks
   for a manager (zero-touch defaults), and automatic authorization adopts it;
   `set-standalone` plus deleting the entry and unplugging it prevents that
   (FortiLink Guide, p. 322; Lab 3.5).
2. Predict what restoring `fgt1-pre-174.conf` on FGT-1 does to a firewall policy
   that someone added for another project after Chapter 02. **Answer:** it
   disappears, like every change since the backup; that is why the manual path
   comes first.

**Expected result:** Track 1: every switch is at factory defaults and powered
off, with no entry, discovery-list, or trusted-list record left on the
controller; the controller's configuration matches its pre-volume file except
for recorded, non-lab differences (or it was restored from that file); on C2
`port3` serves VLAN 202 again, on C3 `port4` is gone; `vmbrFL`, the helper
script, and (Option B) the passthrough settings are gone; VM 174 is destroyed
or stopped as you chose; the Nexus ports are shut and unconfigured; the hosts
hold nothing of the volume; and the final checklist is complete. Track 2: the
stand-in entry and every controller object are gone, `net2` is back on VLAN 202
with its link up (C2), and the controller matches its pre-volume file.

**Negative test:** Look for anything of the lab that should no longer exist:

```text
FGT # show system interface fsw-users
FGT # show switch-controller switch-profile fsw-174-prof
FGT # execute ping 10.255.1.2
```

Each `show` reports that the entry is not found (or prints nothing), and the
ping to the old switch address fails. Track 2: the same three commands.

**Rollback:** None: the teardown ends the volume. To build the lab again, start
at Chapter 02 from the pre-volume configuration.

**The final checklist:**

| Area | Check | Done |
| --- | --- | --- |
| Switches | `FSW-A` (and `FSW-B` on S3) reset to factory defaults, unplugged, powered off; any borrowed switch from Lab 6.2 returned | |
| Controller entries | No managed-switch entry (Track 2: no stand-in); `disable-discovery` and the CSF trusted list hold none of your serials | |
| Controller objects | No `fsw-*` interfaces, `FSW-LAN`, `P2-fortilink-services`, `P3-snmp-174`, `lab-svc-174`, `radius-174`, `ubuntu-ws`, `fsw-lan-174`, `dot1x-174`, security policies, `fsw-174-prof`, `la-174`, `storm-uu-174`, SNMP, sFlow, flow-tracking, or `remote-log` settings of the lab; STP settings back; images deleted | |
| Controller interface | C2: `port3` back in VLAN 202 with its policies and DHCP server; C3: `port4` gone; C1: `<FL_PORT>` back as in `c1-fgt-base-174.conf`, or the unit reset | |
| Comparison | `diff` against the pre-volume file shows no lab line, or the file was restored | |
| Proxmox | C2 `net2` on `vmbr2` tag 202, link up, no `hostpci0`; C3 no `net3` or `hostpci0`; no `vmbrFL`; no `/root/fl-path-check.sh`; vfio list removed (Option B, if unused) | |
| VMs | VM 174 destroyed (or stopped and kept on purpose); VM 140 holds only the files you chose to keep | |
| Nexus | `Eth1/<free>` (and C1's two ports) shut, no description, no access VLAN, no edge setting; configuration saved | |
| Hosts | `ubuntu-ws` without `10-fsw-174.conf`, the trap line, the watcher, or the lab packages; endpoint A without `wired-174.conf`; endpoint B without `10.174.43.20` and the lab packages; console captures kept or deleted on purpose | |
| VLAN 202 (C2) | `execute ping <TEST202_IP>` from FGT-1 succeeds | |

**Lab verified by:** *pending*

## Lab Verification

Complete this sign-off once Labs 12.1 to 12.6 have been run end to end,
including each negative test, every induced fault and its reversal, and the
final checklist. Until then, the labs are unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

A managed switch can be read from the controller and from its own console; the
controller's `switch-info` views need the FortiLink session, the switch's views
do not. Telemetry leaves the switch through the controller's policies: syslog,
traps, sFlow, and flow export ride P2 outward, and SNMP polling needs its own
policy inward, which on C2 is the last free slot. Packets can be captured on
the FortiGate, on the switch itself (not on the FS-108F), by a local mirror,
and by RSPAN (200 Series only). The FortiLink Guide 7.6.7 has no
troubleshooting chapter, so the fault clinic built each signature from
documented output shapes and recorded the rest. Hardening in FortiLink mode is
done with controller objects, and the feature matrix's standalone-only marks
leave remote admin authentication, reliable syslog, and the switch's NTP server
as recorded exceptions. Finally, the teardown retired the switches with
`set-standalone` and a last factory reset, returned the controllers to the
Chapter 02 files, and undid every Proxmox, Nexus, VM, and host change the
volume made.

- [ ] I read the MAC table, LLDP neighbors, port statistics, cable test, and
      topology from both the controller and the switch.
- [ ] I polled the switch with SNMPv3, received a trap, and (S2, S3) received
      sFlow samples and flow records on `ubuntu-ws`.
- [ ] I captured traffic with the FortiGate sniffer, on the switch (S2, S3),
      with a port mirror, and (S3) with RSPAN, and removed every capture and
      mirror.
- [ ] I induced and reverted the cable, LLDP, neighbor-detection,
      deauthorization, and (S3) ICL faults, recorded each signature, and
      predicted the VDOM and firmware faults.
- [ ] I hardened the switch and filled in every row of the evidence table,
      exceptions included.
- [ ] I retired every switch, returned the controller to its pre-volume file,
      undid the Proxmox, Nexus, VM, and host changes, and completed the final
      checklist.
