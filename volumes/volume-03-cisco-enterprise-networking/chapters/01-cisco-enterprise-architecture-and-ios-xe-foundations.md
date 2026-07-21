# Chapter 01: Cisco Enterprise Architecture and IOS XE Foundations

![Lab flow for this chapter: a Catalyst 9000 switch starting in bundle mode is converted to install mode and reloaded, then hardened with a hostname, local credentials, and SSH/console/vty lockdown as CAMPUS-ACCESS-01; VLAN 99 and its SVI (10.10.99.10/24) are created and confirmed up with a successful gateway ping, then Smart Licensing is registered against CSSM. As a negative test, an SSH login with an intentionally wrong password is rejected after three attempts and the failure is confirmed in the device's logging output.](../../../diagrams/volume-03-cisco-enterprise-networking/chapter-01-catalyst-9000-bringup-flow.svg)

*Figure 1-1. Flow used throughout this chapter's Hands-On Lab: bringing a Catalyst 9000 switch from factory defaults to a hardened, licensed, install-mode device.*

## Learning Objectives

- Describe the Cisco Enterprise Architecture model and map its functional
  blocks to the volumes and chapters that follow.
- Explain the hierarchical (access/distribution/core) and routed-access
  design patterns used in modern Catalyst campus networks.
- Identify the Catalyst 9000 hardware family, its silicon architecture, and
  the criteria used to size a platform for a given role.
- Distinguish IOS XE **install mode** from **bundle mode** and explain why
  install mode is the operational standard on Catalyst 9000 switches.
- Configure Smart Licensing Using Policy (SLP) and interpret its status
  output.
- Perform an initial, secure bring-up of a Catalyst 9000 switch, including
  day-0 hardening steps.

## Theory and Architecture

### The Cisco Enterprise Architecture model

Cisco's Enterprise Architecture decomposes a customer network into functional
blocks so that design, capacity planning, and operational ownership can be
reasoned about independently while still interoperating as one system. The
canonical blocks are:

| Block | Function | Primary volume coverage |
| --- | --- | --- |
| Enterprise Campus | Wired/wireless access for users and endpoints, campus core | Volume III (this volume) |
| Enterprise Branch | Remote-site LAN plus WAN attachment | [Volume III, Chapter 4](04-enterprise-wan-internet-edge-and-catalyst-sd-wan.md) |
| WAN / Internet Edge | Site-to-site transport, internet peering, perimeter | [Volume III, Chapter 4](04-enterprise-wan-internet-edge-and-catalyst-sd-wan.md) |
| Data Center | Server and application connectivity | [Volume VI](../../volume-06-enterprise-storage-data-protection/README.md), [Volume VIII](../../volume-08-containers-platform-engineering/README.md) |
| Enterprise Cloud | Public/hybrid cloud connectivity | [Volume VII](../../volume-07-cloud-infrastructure/README.md) |

This volume focuses on the Enterprise Campus, Branch, and WAN blocks as
implemented on Cisco Catalyst switching and routing running IOS XE. Cisco
Validated Designs (CVDs) and the SAFE security reference architecture
overlay this same model with security control placement guidance; this
volume references SAFE concepts where they affect switch and router
configuration, and defers deep security architecture to [Volume X](../../volume-10-enterprise-cybersecurity/README.md).

### Hierarchical campus design

The classic three-tier hierarchical model separates the campus into:

- **Access layer** — the tier where endpoints (workstations, phones, access
  points, IoT devices) physically connect. Access switches enforce
  port-level policy: VLAN assignment, 802.1X, port security, QoS trust
  boundaries, and PoE delivery.
- **Distribution layer** — aggregates access switches, is the typical
  boundary between Layer 2 and Layer 3, hosts first-hop redundancy
  protocols, and applies route summarization and policy before traffic
  enters the core.
- **Core layer** — a high-speed, low-latency backbone whose only job is to
  switch/route packets between distribution blocks and to the WAN/data
  center edge as fast as possible. Cores generally carry no endpoint
  policy.

A **two-tier collapsed core** design merges the distribution and core
functions on the same pair of switches — common in mid-size campuses and
branch sites where a dedicated core is not justified by scale.

**Routed access** extends Layer 3 all the way to the access switch (the
access-to-distribution uplink runs a routing protocol instead of a trunk).
Routed access removes Spanning Tree Protocol (STP) convergence time from the
access-to-distribution boundary, at the cost of requiring a routed uplink
and per-VLAN SVIs (or /30 or /31 point-to-point links) on every access
switch. [Chapter 2](02-catalyst-campus-switching-and-resiliency.md) covers the traditional Layer-2 access alternative and the
STP toolkit that secures it; [Chapter 9](09-catalyst-center-sd-access-assurance-and-operations.md) covers the SD-Access fabric overlay,
which is a distinct, policy-driven evolution of the same physical topology.

### IOS XE platform architecture

Cisco IOS XE is a Linux-based operating system in which the traditional IOS
control-plane binary runs as a protected process (`IOSd`) alongside other
platform processes (chassis management, packaging, licensing, telemetry)
under a Linux kernel. This separation is what enables:

- **Process-level resiliency** — a crash in a non-IOSd process does not
  necessarily reload the switch.
- **In-Service Software Upgrade (ISSU)** and **In-Service Software
  Downgrade (ISSD)** on platforms with redundant supervisors or StackWise
  Virtual, reducing planned-maintenance downtime.
- **Native containers and guest shell** — a Linux application space that
  hosts Python scripting, third-party container workloads, and on-box
  automation tooling ([Chapter 8](08-ios-xe-programmability-and-network-automation.md)).
- **Streaming telemetry and model-driven programmability** — YANG-modeled
  configuration and operational state exposed over NETCONF, RESTCONF, and
  gNMI ([Chapter 8](08-ios-xe-programmability-and-network-automation.md)), alongside the traditional CLI.

Catalyst 9000 switches forward traffic using Cisco's custom silicon: the
Unified Access Data Plane (UADP) ASIC family on the Catalyst 9200, 9300,
9400, and (Supervisor-1) 9500/9600 series, and Cisco Silicon One on
select higher-density Catalyst 9600 supervisor and line-card options. UADP's
programmable pipeline is what allows features such as SD-Access VXLAN
encapsulation, flexible NetFlow, and MACsec line-rate encryption to be added
through software without a forklift hardware upgrade.

### Catalyst 9000 family and stacking

| Platform | Typical role | Stacking / redundancy |
| --- | --- | --- |
| Catalyst 9200 / 9200L | Branch and lean access | StackWise-160 |
| Catalyst 9300 / 9300X | Campus access, small distribution | StackWise-480 (9300), StackWise-1T (9300X) |
| Catalyst 9400 | Modular access/distribution | Dual supervisor, StackWise Virtual (SVL) |
| Catalyst 9500 | Distribution, small/medium core | StackWise Virtual (SVL) |
| Catalyst 9600 | Large campus core | Dual supervisor, StackWise Virtual (SVL) |

**StackWise-480** and **StackWise-1T** physically stack fixed-configuration
switches with a dedicated stacking backplane, presenting the stack as one
logical switch with one control plane (active) and one standby. **StackWise
Virtual (SVL)** achieves the same logical-single-switch behavior across two
chassis-based or fixed switches using standard high-speed Ethernet ports as
the SVL link plus a separate dual-active detection (DAD) link — this is the
mechanism used at the distribution/core tier where physical stacking
backplanes are not available.

### Boot process and software packaging

On first power-up, the switch's ROMMON bootloader locates a valid IOS XE
package set (either a monolithic `.bin` bundle or an extracted `packages.conf`
provisioning file), verifies its checksum, and hands off to IOS XE. Two
packaging modes exist:

- **Bundle mode** boots directly from the consolidated `.bin` file on flash.
  It is simpler but does not support ISSU and re-verifies/decompresses the
  full image on every boot, which is slower.
- **Install mode** extracts the bundle into individual package files plus a
  `packages.conf` pointer file, and boots from those extracted packages.
  Install mode is required for ISSU/ISSD, supports Smart Licensing Using
  Policy cleanly, and boots faster after the initial conversion. Cisco ships
  Catalyst 9000 switches in install mode by default and it is the
  operational standard referenced throughout this volume.

## Design Considerations

- **Tier collapsing** — collapse distribution and core into a two-tier
  design only when the campus is small enough that a dedicated core layer
  would sit idle; document the decision, since re-introducing a core later
  is disruptive.
- **Routed vs. switched access** — choose routed access when fast
  convergence and VLAN/broadcast-domain containment outweigh the
  operational simplicity of trunked access; choose switched (Layer 2)
  access when VLANs must span multiple access switches (for example,
  legacy voice VLAN designs or applications requiring Layer 2 adjacency).
- **Platform sizing** — size access switches on port count, PoE budget
  (PoE+, UPOE, UPOE+), and uplink bandwidth (multigigabit uplinks matter
  more than downlink speed in most refreshes); size distribution/core on
  aggregate throughput, buffer depth, and the number of routed uplinks/ECMP
  paths required.
- **Redundancy model** — a single StackWise-480 stack removes the need for
  First Hop Redundancy Protocol (FHRP) at the access layer ([Chapter 2](02-catalyst-campus-switching-and-resiliency.md)) but
  creates a shared fate for the whole stack during a software upgrade
  unless ISSU is used; StackWise Virtual and dual supervisors extend this
  same trade-off to the distribution/core tier.
- **Licensing tier** — Network Essentials covers base Layer 2/3 switching;
  Network Advantage is required for advanced features such as StackWise
  Virtual on certain platforms, full BGP scale, and is a prerequisite for
  the DNA/Catalyst Center subscription tiers that unlock SD-Access,
  Assurance, and advanced automation ([Chapter 9](09-catalyst-center-sd-access-assurance-and-operations.md)). Confirm the required tier
  against the current Cisco ordering guide before design sign-off, since
  feature-to-tier mapping changes between releases.
- **Licensing model** — Smart Licensing Using Policy is the current default
  on IOS XE 17.x; plan for connectivity to Cisco Smart Software Manager
  (CSSM) directly, via a Smart Licensing satellite/Cisco Smart Software
  Manager On-Prem, or via a manually synchronized offline workflow for
  air-gapped networks.
- **Management network separation** — plan a dedicated out-of-band
  management VLAN/subnet reachable from the NOC independent of the
  production forwarding path, so that a campus-wide routing or STP event
  does not also strand management access.

## Implementation and Automation

### Verifying and converting to install mode

```text
Switch# show version | include Installation Mode
Switch# show install summary
```

If the switch is running in bundle mode, convert it to install mode:

```text
Switch# request platform software package install switch all file flash:cat9k_iosxe.17.09.05a.SPA.bin new install_mode
```

The switch extracts the packages, writes `packages.conf`, and reloads
automatically to boot from the extracted set.

### Initial device bring-up

```text
Switch> enable
Switch# configure terminal
Switch(config)# hostname CAMPUS-ACCESS-01
CAMPUS-ACCESS-01(config)# ip domain-name example.internal
CAMPUS-ACCESS-01(config)# username netadmin privilege 15 algorithm-type scrypt secret <STRONG_PASSWORD>
CAMPUS-ACCESS-01(config)# enable algorithm-type scrypt secret <STRONG_ENABLE_SECRET>
CAMPUS-ACCESS-01(config)# crypto key generate rsa modulus 2048 label CAMPUS-ACCESS-01.example.internal
CAMPUS-ACCESS-01(config)# ip ssh version 2
CAMPUS-ACCESS-01(config)# line vty 0 15
CAMPUS-ACCESS-01(config-line)# transport input ssh
CAMPUS-ACCESS-01(config-line)# login local
CAMPUS-ACCESS-01(config-line)# exec-timeout 10 0
CAMPUS-ACCESS-01(config-line)# exit
CAMPUS-ACCESS-01(config)# line console 0
CAMPUS-ACCESS-01(config-line)# exec-timeout 10 0
CAMPUS-ACCESS-01(config-line)# logging synchronous
CAMPUS-ACCESS-01(config-line)# exit
CAMPUS-ACCESS-01(config)# interface Vlan1
CAMPUS-ACCESS-01(config-if)# no ip address
CAMPUS-ACCESS-01(config-if)# shutdown
CAMPUS-ACCESS-01(config-if)# exit
CAMPUS-ACCESS-01(config)# vlan 99
CAMPUS-ACCESS-01(config-vlan)# name MGMT
CAMPUS-ACCESS-01(config-vlan)# exit
CAMPUS-ACCESS-01(config)# interface Vlan99
CAMPUS-ACCESS-01(config-if)# description Out-of-band management
CAMPUS-ACCESS-01(config-if)# ip address 10.10.99.10 255.255.255.0
CAMPUS-ACCESS-01(config-if)# no shutdown
CAMPUS-ACCESS-01(config-if)# exit
CAMPUS-ACCESS-01(config)# ip default-gateway 10.10.99.1
```

Note that `ip default-gateway` only applies when the switch has no IP
routing enabled (`no ip routing`, the Layer 2 default). On a Layer 3 switch
running `ip routing`, use a static or dynamic default route instead
([Chapter 3](03-cisco-enterprise-routing-and-path-control.md)).

### Smart Licensing Using Policy

```text
CAMPUS-ACCESS-01(config)# license smart transport smart
CAMPUS-ACCESS-01(config)# license smart url default
CAMPUS-ACCESS-01(config)# exit
CAMPUS-ACCESS-01# license smart trust idtoken <TOKEN_FROM_CSSM> all
CAMPUS-ACCESS-01# show license status
CAMPUS-ACCESS-01# show license summary
```

For air-gapped networks, use offline reporting instead of a direct CSSM
transport:

```text
CAMPUS-ACCESS-01# license smart save usage all file bootflash:license-usage.txt
```

Upload the resulting RUM report file to CSSM manually or through a Smart
Software Manager On-Prem instance, per the current Cisco licensing guide.

### Day-0 configuration at scale

For fleet bring-up, pair a day-0 template with a Python/Ansible workflow
(introduced fully in [Chapter 8](08-ios-xe-programmability-and-network-automation.md)) rather than typing each switch by hand.
A minimal day-0 template file suitable for PnP or a bootstrap TFTP/USB
provisioning workflow should set hostname, management IP, local admin
credentials, SSH, and NTP as an absolute minimum before the device is
handed off to the automation platform for policy convergence.

## Validation and Troubleshooting

```text
CAMPUS-ACCESS-01# show version
CAMPUS-ACCESS-01# show switch
CAMPUS-ACCESS-01# show platform
CAMPUS-ACCESS-01# show install summary
CAMPUS-ACCESS-01# show license summary
CAMPUS-ACCESS-01# show environment all
CAMPUS-ACCESS-01# show processes cpu sorted | exclude 0.00%  0.00%  0.00%
CAMPUS-ACCESS-01# show logging | include %PLATFORM|%SYS-
```

Common issues and diagnostics:

| Symptom | Likely cause | Check |
| --- | --- | --- |
| Switch stuck in ROMMON | Corrupted or missing boot image | `dir flash:`, reload valid image via `boot flash:<file>` at ROMMON prompt |
| `show install summary` shows bundle mode after conversion command | Conversion command syntax error or insufficient flash space | `dir flash:`, retry with `new install_mode` keyword and confirm free space exceeds image size |
| SSH access refused | RSA key not generated, or `transport input` not set to `ssh` | `show ip ssh`, `show crypto key mypubkey rsa` |
| License shows `EVAL EXPIRED` or `OUT OF COMPLIANCE` | No CSSM connectivity or trust token not installed within the reporting window | `show license status`, verify transport reachability and re-run `license smart trust idtoken` |
| Stack member shows `V-Mismatch` in `show switch` | Members running different IOS XE versions | Upgrade the mismatched member via `software install` targeted at that switch number |

## Security and Best Practices

- Disable unused physical and logical access: shut down unused interfaces,
  disable VLAN 1 as the native/management VLAN, and remove `ip http server`
  unless RESTCONF/webUI is explicitly required (prefer `ip http secure-server`
  when a management UI is needed).
- Enforce local or AAA-backed authentication with `login local` or
  TACACS+/RADIUS ([Chapter 7](07-cisco-identity-access-control-and-segmentation.md)) — never leave default or blank credentials on
  a device that will be racked in production.
- Set `service password-encryption` as a minimum baseline, but prefer
  `algorithm-type scrypt secret` for all local passwords, since weak
  reversible/type-7 encryption should never protect a production credential.
- Apply Control Plane Policing (CoPP) so that a flood or misconfiguration on
  the data plane cannot starve the IOSd control plane; Cisco ships a default
  CoPP policy on Catalyst 9000, but validate it matches your traffic profile
  rather than assuming the default is sufficient for your environment.
- Keep the software train aligned with Cisco's IOS XE release model
  (Standard Maintenance Deployment releases for planned refresh cycles,
  Extended Maintenance Deployment releases for long-lived production
  stability) and track published Cisco Security Advisories via the Cisco
  Security Advisories page for the running train.
- Maintain configuration backups (`copy running-config` to a controlled
  repository) before and after every change window; treat the
  running-configuration as the source of truth only until it is captured
  under version control ([Volume IX](../../volume-09-infrastructure-automation/README.md)).

## References and Knowledge Checks

**Authoritative references**

- Cisco, *Catalyst 9000 Switching Platform* data sheets and ordering guides
  (cisco.com).
- Cisco, *IOS XE Software Installation and Upgrade Guide*, current release
  train documentation.
- Cisco, *Smart Licensing Using Policy* configuration guide.
- Cisco Enterprise Architecture and SAFE reference documentation.

**Knowledge checks**

1. What distinguishes install mode from bundle mode, and why does ISSU
   require install mode?
2. In a collapsed two-tier design, which classic three-tier function is
   absorbed into the distribution/core switches?
3. What is the functional difference between StackWise-480 and StackWise
   Virtual, and when would you choose one over the other?
4. Which licensing tier is generally required as a prerequisite for
   SD-Access and Catalyst Center Assurance features, and why does that
   matter during procurement?
5. Why does `ip default-gateway` fail to take effect on a switch running
   `ip routing`?

## Hands-On Lab

**Objective:** Bring up a Catalyst 9000 switch (physical lab or a Cisco
Modeling Labs / CML topology using the Catalyst 9000v or IOL Layer-3 node)
from factory defaults to a hardened, licensed, install-mode device.

**Prerequisites**

- One Catalyst 9000-series switch (or CML node) with console access.
- A laptop with a terminal emulator and, if using CML, network reachability
  to the lab's management network.
- A valid IOS XE install-mode image on flash (physical lab) or pre-loaded
  in the CML node definition.
- Optional: CSSM Smart Account access for the licensing steps; skip the
  transport step and use `show license status` only if no account is
  available.

**Procedure**

1. Console into the switch and confirm the current boot mode:

   ```text
   Switch> enable
   Switch# show version | include Installation Mode
   ```

2. If the switch reports bundle mode, list flash contents and convert to
   install mode:

   ```text
   Switch# dir flash:
   Switch# request platform software package install switch all file flash:<image>.bin new install_mode
   ```

   The switch reloads automatically. Reconnect after reload.

3. Set the hostname, local credentials, SSH, and console/vty hardening as
   shown in the Implementation section above, substituting your own lab
   naming convention and a strong password.

4. Create the management VLAN and interface, and confirm connectivity:

   ```text
   CAMPUS-ACCESS-01# show vlan brief | include 99
   CAMPUS-ACCESS-01# show ip interface brief | include Vlan99
   CAMPUS-ACCESS-01# ping 10.10.99.1
   ```

   **Expected result:** VLAN 99 shows as active, `Vlan99` shows `up/up`
   with the configured address, and the gateway ping succeeds (or reports
   destination-unreachable in an isolated lab with no gateway present,
   which still confirms the interface is forwarding).

5. Register Smart Licensing (skip if no CSSM access is available in the
   lab):

   ```text
   CAMPUS-ACCESS-01(config)# license smart transport smart
   CAMPUS-ACCESS-01(config)# license smart url default
   CAMPUS-ACCESS-01(config)# exit
   CAMPUS-ACCESS-01# license smart trust idtoken <TOKEN> all
   CAMPUS-ACCESS-01# show license status
   ```

   **Expected result:** `show license status` reports the transport type
   and a recent, successful last report/sync attempt.

6. **Negative test:** attempt SSH login with an intentionally incorrect
   password from your terminal:

   ```text
   ssh netadmin@10.10.99.10
   ```

   **Expected result:** authentication is rejected after three attempts and
   the session is closed; confirm the failure is logged:

   ```text
   CAMPUS-ACCESS-01# show logging | include Login
   ```

7. Save the running configuration and archive it off-device:

   ```text
   CAMPUS-ACCESS-01# copy running-config startup-config
   CAMPUS-ACCESS-01# copy startup-config tftp:
   ```

**Cleanup**

- If this is a shared lab switch, restore factory defaults before handing
  it back:

  ```text
  CAMPUS-ACCESS-01# write erase
  CAMPUS-ACCESS-01# reload
  ```

- In CML, delete or reset the lab topology once validation evidence has
  been captured.

## Lab Verification

Complete this sign-off once the lab has been run end to end, including the
negative test. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

This chapter mapped the Cisco Enterprise Architecture model to the rest of
this volume, walked through the hierarchical campus design patterns that
every later chapter builds on, and established the IOS XE platform
fundamentals — process architecture, UADP/Silicon One forwarding, install
mode, stacking options, and Smart Licensing Using Policy — that underpin
every subsequent configuration example in this volume.

- [ ] Can explain the Cisco Enterprise Architecture blocks and where this
      volume fits.
- [ ] Can compare three-tier vs. collapsed two-tier vs. routed-access
      designs and state a reason to choose each.
- [ ] Can identify install mode vs. bundle mode and convert a switch
      between them.
- [ ] Can bring up a Catalyst 9000 switch with hardened management access
      and register it with Smart Licensing Using Policy.
- [ ] Completed the hands-on lab, including the negative authentication
      test and cleanup steps.
