# Chapter 05: Storage Networking: Fibre Channel, FCoE, and NVMe

## Learning Objectives

- Explain Fibre Channel's fabric services and login sequence, and why
  the SAN's discipline differs from Ethernet's
- Configure VSANs, zoning, and device aliases on MDS, and NPV/NPIV at
  the edge
- Describe FCoE's encapsulation and the lossless Ethernet machinery
  (PFC, ETS, DCBX) it depends on
- Position NVMe over Fabrics — FC-NVMe and NVMe/TCP — against SCSI
  transports
- Validate fabric logins, zoning, and end-to-end storage reachability,
  and troubleshoot the classic SAN faults

## Theory and Architecture

### Fibre Channel: the network that never learned to drop

Storage traffic's defining requirement is losslessness: a dropped
frame is not a retransmit, it is an I/O error a filesystem remembers.
Fibre Channel achieves it with **buffer-to-buffer credits** — a
transmitter sends only when the receiver has advertised buffer space —
and organizes the fabric with services Ethernet never had built in:
the **name server** (what is attached and what it can do), the domain
controller (switch addressing), and **zoning** (who may talk to whom).

The login sequence is the exam's favorite ordering question and the
field's favorite troubleshooting ladder: **FLOGI** (N_Port to fabric —
get an FCID), **PLOGI** (port to port), **PRLI** (process login —
SCSI/NVMe capability exchange). `show flogi database` and
`show fcns database` answer "did it login" and "did the fabric learn
what it is" respectively, and between them locate most faults.

### Structure: VSANs, zones, and the dual-fabric religion

- **VSANs** slice one physical fabric into isolated logical fabrics —
  separate services, separate zoning — the storage analog of VRFs.
- **Zoning** permits initiator-target pairs. Modern practice:
  **device aliases** for names (they follow the WWPN, unlike zone
  aliases which are VSAN-scoped), single-initiator-single-target zones
  or **smart zoning** on MDS to get equivalent enforcement from
  friendlier configuration, and *enhanced zoning* so changes commit
  atomically fabric-wide.
- **Dual independent fabrics** (A and B) with hosts multipathed across
  both is not a design choice, it is the design: no shared components,
  no shared mistakes, maintenance without downtime.

### NPV and NPIV: scaling the edge

**NPIV** lets one physical N_Port carry many logins (virtual machines,
or the virtual HBAs Chapter 04's profiles create). **NPV** puts an
edge switch in host mode: it forwards logins upstream instead of
consuming a domain ID and running fabric services — which is exactly
how UCS fabric interconnects attach to the SAN by default. The pairing
is the standard modern edge: NPV switches at the access, NPIV-enabled
core carrying the logins.

### FCoE and the lossless Ethernet toolkit

FCoE encapsulates full FC frames in Ethernet, letting the unified
fabric carry SAN and LAN on one wire — the economics that power UCS
internally. Because FC assumes losslessness, the Ethernet underneath
must fake it: **PFC** (per-priority pause, so the storage class never
drops while others may), **ETS** (bandwidth allocation between
classes), and **DCBX** (negotiating both with the peer). FIP, the
initialization protocol, discovers FCFs and establishes the virtual
links. FCoE's field footprint concentrated inside UCS domains and
top-of-rack; its concepts — traffic classes that must not drop —
return with force in Chapter 07, where RoCE for AI clusters needs the
identical machinery.

### NVMe over Fabrics

SCSI's command model predates flash; NVMe's queues-per-core design is
built for it, and extending NVMe across the fabric removes the SCSI
translation from the path. **FC-NVMe** runs on existing FC fabrics —
same zoning discipline, PRLI advertising NVMe capability — making it
the natural upgrade for MDS estates. **NVMe/TCP** trades some latency
for running on any IP network. **NVMe/RoCE** delivers the lowest
latency and inherits the lossless-Ethernet requirements above. DCCOR's
storage domain expects positioning fluency more than packet formats:
know which transport fits which estate and why.

## Design Considerations

- Fabric A/B separation carried literally everywhere: separate MDS
  pairs, separate vHBA templates, separate uplinks — a single shared
  anything is the design flaw.
- **Oversubscription is calculated, not felt**: host edge to ISL
  ratios sized from actual storage throughput, with port-channel ISLs
  and credits watched (`show interface ... counters` for credit
  starvation, the SAN's congestion signature).
- Zone from device aliases with smart zoning; retrofit-cleaning a
  fabric of ad-hoc WWPN zones is a project, not a task.
- For new latency-sensitive estates, FC-NVMe on existing fabric
  discipline is the conservative modernization; NVMe/TCP where FC
  does not exist and the latency budget allows.

## Implementation and Automation

MDS-side build for a dual-fabric SAN serving Chapter 04's SAN-boot
profiles:

```text
feature npiv
vsan database
  vsan 10 name FABRIC-A
  vsan 10 interface fc1/1-8

device-alias database
  device-alias name ESX1-HBA-A pwwn 20:00:00:25:b5:aa:00:01
  device-alias name ARRAY-CTL-A pwwn 50:06:01:60:3e:a0:12:34
device-alias commit

zone smart-zoning enable vsan 10
zone name Z-ESX1-ARRAY vsan 10
  member device-alias ESX1-HBA-A initiator
  member device-alias ARRAY-CTL-A target
zoneset name ZS-FABRIC-A vsan 10
  member Z-ESX1-ARRAY
zoneset activate name ZS-FABRIC-A vsan 10
```

```text
# Validation ladder
show flogi database                    # did the HBA login (FLOGI)?
show fcns database vsan 10             # does the name server know it?
show zoneset active vsan 10            # is the zone active?
show device-alias database
# On the UCS side (Chapter 04): the vHBA's WWPN should appear here.
```

Automation: MDS speaks NX-API like its Nexus siblings; zoning changes
are prime automation targets because they are frequent, patterned, and
audit-hungry (Chapter 06 builds the playbook).

## Validation and Troubleshooting

The ladder above is the method: a missing FLOGI is physical/port/VSAN
membership; FLOGI present but FCNS empty of capabilities means PRLI
problems (driver, or NVMe capability absent); everything present but
no storage means zoning (member spelled by alias? zoneset *activated*,
not merely configured?) or masking on the array. Credit starvation
shows as B2B credit-zero counters climbing on ISLs — a congestion
problem, not a login problem, solved by paths and speed, not zoning.
For FCoE, DCBX mismatches (PFC class disagreement) present as
mysterious storage stalls under load: `show lldp dcbx interface ...`
before blaming the array.

## Security and Best Practices

- Zoning is access control; default-zone permit is the SAN's
  "permit any" and stays off.
- Port security (WWPN binding) on host-facing F_Ports where the
  physical environment warrants; fabric binding between switches.
- The SAN management plane gets the same AAA and out-of-band
  discipline as everything else — an MDS admin session can unzone a
  production array.

## References and Knowledge Checks

- Cisco MDS 9000 configuration guides (fabric, zoning, FCoE, FC-NVMe)
- DCCOR 350-601 v1.2 Storage Network domain (20%); DCID storage design
  domain (20%)
- FC-NVMe and NVMe/TCP standards overviews (NVM Express)

Knowledge checks:

1. Order and explain FLOGI, PLOGI, PRLI — and name the show command
   that proves each stage.
2. Why does an NPV edge switch consume no domain ID, and what problem
   does that solve at scale?
3. PFC pauses one traffic class. Why is that essential for FCoE and
   RoCE, and what happens with a DCBX mismatch?
4. A host sees the fabric but not its LUN. Walk the ladder — which
   two layers remain after FCNS shows the target's capabilities?

## Hands-On Lab

This chapter carries a topic-level walkthrough lab for **every objective in
Domain 3 (Storage Network) of DCCOR 350-601 v1.2 and every objective of the
DCSAN 300-625 v1.0 exam guide** — Fibre Channel, FCoE, VSANs, zoning, IVR,
DCNM, and MDS troubleshooting — mapped in the volume README's coverage
tables. Labs use the MDS/Nexus NX-OS storage CLI and DCNM/NDFC. Each ends
**`**Lab verified by:** *pending*`** until a human runs it.

**Shared prerequisites for Labs 5.1–5.22** — an MDS 9000 (or Nexus with the
FC/FCoE feature set) fabric with at least two switches, initiators and targets
logged in, DCNM/NDFC reachable at `$DCNM`, and console access for the
boot/upgrade labs. **Cost:** none beyond lab resources.

### Lab 5.1 — Implement Fibre Channel (DCCOR Objective 3.1)

**Objective:** Bring up an FC interface and confirm the port and fabric login.

```text
config t
 feature fcoe
 interface fc1/1
  no shutdown
end
show interface fc1/1 brief
show flogi database
```

**Expected result:** `fc1/1` in `up` with a port mode (F/E/NP) and the
attached device's FCID and pWWN in the FLOGI database — the fabric login that
admits a device.

**Negative test:** connect an initiator to a port whose VSAN differs from the
target's; FLOGI succeeds but the device cannot reach the target — VSAN
membership isolates the fabric.

**Cleanup:** `interface fc1/1 ; shutdown` if the port was brought up for the
lab.

### Lab 5.2 — Describe network storage systems: NFS and iSCSI (DCCOR Objective 3.2)

**Objective:** Contrast file (NFS) and block-over-IP (iSCSI) reachability from
a host.

```bash
showmount -e 10.0.0.60            # NFS exports
iscsiadm -m discovery -t st -p 10.0.0.61:3260   # iSCSI targets
```

**Expected result:** the NFS exports list and the iSCSI target IQNs — NFS is
file storage over TCP/2049; iSCSI is block storage over TCP/3260, the
IP-fabric alternatives to Fibre Channel.

**Negative test:** discover iSCSI against a portal with no target LUN mapped
to the initiator's IQN; discovery returns the target but `login` yields no
LUNs — access requires initiator-group mapping on the array.

**Cleanup:** `iscsiadm -m node -u` to log out any test session.

### Lab 5.3 — Describe software updates and their impacts: disruptive/nondisruptive and EPLD (DCCOR Objective 3.3)

**Objective:** Run an MDS upgrade impact check including EPLD.

```text
show install all impact kickstart bootflash:m9000-nxos.9.4.bin system bootflash:m9000-nxos.9.4.bin
show install all impact epld bootflash:m9000-epld.9.4.img
```

**Expected result:** a per-module report marking the NX-OS upgrade
`non-disruptive` (ISSU) where supported, and the EPLD update as **disruptive**
— EPLD (hardware programmable logic) updates require a module reload.

**Negative test:** attempt ISSU during an active zone-set change or with a
single supervisor; the impact check reports it as disruptive.

**Cleanup:** none (impact check is read-only).

### Lab 5.4 — Implement infrastructure monitoring with SPAN and Nexus Dashboard (DCCOR Objective 3.4)

**Objective:** Configure an FC SPAN (SD port) session.

```text
config t
 interface fc1/12
  switchport mode SD
 monitor session 1
  source interface fc1/1 rx
  destination interface fc1/12
  no shut
end
show monitor session 1
```

**Expected result:** the SPAN session mirroring FC traffic to the SD port — FC
analysis feeds analyzers and Nexus Dashboard/SAN Insights for congestion
visibility.

**Negative test:** set the destination to a normal F port instead of `SD`;
NX-OS rejects it — FC SPAN destinations must be SD mode.

**Cleanup:** `no monitor session 1` and revert `fc1/12` mode.

### Lab 5.5 — Describe installation and initial setup: NX-OS, DCNM, POAP (DCSAN Objective 1.1)

**Objective:** Read the MDS initial-setup state and POAP status.

```text
show version | include "system:|kickstart:"
show boot
show run | include "boot "
```

**Expected result:** the running kickstart/system images and boot variables —
the initial setup (`setup` script or POAP zero-touch) writes these; DCNM can
push them at scale.

**Negative test:** clear the boot variables and reload; the switch drops to
the `loader>` prompt — boot variables are what make the switch bootable
unattended.

**Cleanup:** none (read-only; do not clear boot variables in production).

### Lab 5.6 — Describe secure boot (DCSAN Objective 1.2)

**Objective:** Confirm image integrity / secure-boot state.

```text
show system secure-boot 2>/dev/null || show version | include "Secure"
show file bootflash:m9000-nxos.9.4.bin sha256sum
```

**Expected result:** secure-boot enabled (anchored in hardware) or the image's
SHA-256 matching Cisco's published hash — the chain that prevents booting a
tampered image.

**Negative test:** compute the hash of a truncated/altered image; it will not
match Cisco's published value — integrity verification catches tampering.

**Cleanup:** none (read-only).

### Lab 5.7 — Implement Fibre Channel port channels (DCSAN Objective 2.1)

**Objective:** Bundle ISLs into an FC port channel.

```text
config t
 interface port-channel 10
  channel mode active
 interface fc1/1-2
  channel-group 10 force
  no shutdown
end
show port-channel database interface port-channel 10
```

**Expected result:** port-channel 10 up with both members — an aggregated ISL
that load-balances FC exchanges and survives a single link loss.

**Negative test:** add a member with a mismatched speed or VSAN allowed list;
it is suspended, not added — port-channel members must be compatible.

**Cleanup:** `no interface port-channel 10`.

### Lab 5.8 — Implement Fibre Channel protocol services: Name Service and CFS (DCSAN Objective 2.2)

**Objective:** Query the fabric name server and confirm CFS distribution.

```text
show fcns database
show cfs status
show cfs merge status name IVR
```

**Expected result:** every logged-in device registered in the name server
(FCID, pWWN, FC4 type) and CFS `Distribution: Enabled` — CFS synchronizes
zoning/IVR config fabric-wide.

**Negative test:** disable CFS distribution for zoning and edit a zone; the
change stays local and a later merge conflicts — CFS is what keeps the fabric
consistent.

**Cleanup:** none (read-only).

### Lab 5.9 — Implement FCoE: FIP, PFC, ETS, DCBX/LLDP (DCSAN Objective 2.3)

**Objective:** Verify the lossless-Ethernet plumbing FCoE requires.

```text
show interface ethernet 1/1 priority-flow-control
show system qos | include "network-qos"
show fcoe database
show lldp dcbx interface ethernet 1/1
```

**Expected result:** PFC enabled on the FCoE priority, ETS bandwidth
allocation, DCBX converged with the CNA, and FCoE sessions in the database —
the four pieces that make Ethernet lossless enough to carry FC.

**Negative test:** disable PFC on the FCoE class; FCoE logins drop under
congestion — without lossless behavior, FC-over-Ethernet fails.

**Cleanup:** none (read-only).

### Lab 5.10 — Implement VSANs (DCSAN Objective 2.4)

**Objective:** Create a VSAN and assign a member interface.

```text
config t
 vsan database
  vsan 100 name PROD-SAN
  vsan 100 interface fc1/1
end
show vsan
show vsan membership
```

**Expected result:** VSAN 100 active with `fc1/1` a member — VSANs partition
one physical SAN into isolated virtual fabrics, each with its own services.

**Negative test:** move an interface to a suspended VSAN; the port goes
`isolated` — membership in an inactive VSAN drops the port.

**Cleanup:** `vsan database ; no vsan 100`.

### Lab 5.11 — Implement NPV and NPIV (DCSAN Objective 2.5)

**Objective:** Read NPV mode on an edge switch and NPIV on the core.

```text
show npv status
show npv flogi-table
show feature | include npiv
```

**Expected result:** the edge switch in NPV mode proxying host FLOGIs upstream
(`show npv flogi-table`) and NPIV enabled on the core F port — NPV avoids
consuming domain IDs; NPIV lets multiple logins share a port.

**Negative test:** connect an NPV edge to a core with NPIV disabled; host
logins fail — the core must accept multiple logins on the proxied port.

**Cleanup:** none (read-only).

### Lab 5.12 — Implement device aliases and zoning (DCSAN Objective 2.6)

**Objective:** Create a device alias and a single-initiator zone, then
activate.

```text
config t
 device-alias database
  device-alias name HOST1 pwwn 10:00:00:00:c9:aa:bb:cc
  device-alias name ARRAY1 pwwn 50:06:01:60:aa:bb:cc:dd
 device-alias commit
 zone name HOST1-ARRAY1 vsan 100
  member device-alias HOST1
  member device-alias ARRAY1
 zoneset name ZS-PROD vsan 100
  member HOST1-ARRAY1
 zoneset activate name ZS-PROD vsan 100
end
show zoneset active vsan 100
```

**Expected result:** the active zoneset with the single-initiator zone and an
asterisk on logged-in members — access control by pWWN, the SAN's segmentation.

**Negative test:** activate a zoneset with two initiators in one zone; it works
but is a design fault (cross-talk risk) — single-initiator zoning is the
best-practice the negative highlights.

**Cleanup:** deactivate the test zoneset and remove the zone/aliases.

### Lab 5.13 — Configure inter-VSAN routing (DCSAN Objective 2.7)

**Objective:** Build an IVR zone to share a target across two VSANs.

```text
config t
 ivr nat
 ivr vsan-topology auto
 ivr zone name IVR-HOST-ARRAY
  member pwwn 10:00:00:00:c9:aa:bb:cc vsan 100
  member pwwn 50:06:01:60:aa:bb:cc:dd vsan 200
 ivr zoneset name IVR-ZS
  member IVR-HOST-ARRAY
 ivr zoneset activate name IVR-ZS
end
show ivr zoneset active
show ivr fcdomain database
```

**Expected result:** the active IVR zoneset and the IVR domain database — IVR
with NAT lets a host in VSAN 100 reach a target in VSAN 200 without merging the
fabrics.

**Negative test:** enable IVR without NAT across overlapping domain IDs; IVR
reports a domain conflict — NAT (or unique domains) is required.

**Cleanup:** deactivate `IVR-ZS` and remove the IVR configuration.

### Lab 5.14 — Implement VSAN extensions (DCSAN Objective 2.8)

**Objective:** Read an FCIP tunnel that extends a VSAN over IP.

```text
show interface fcip 1
show fcip summary
show interface fcip 1 counters brief
```

**Expected result:** the FCIP tunnel `up` carrying an FC VSAN over an IP WAN —
the extension used for remote replication between data centers.

**Negative test:** an FCIP tunnel with mismatched MTU or high WAN latency and
no FC write-acceleration shows degraded throughput — distance and tuning
matter for VSAN extension.

**Cleanup:** none (read-only).

### Lab 5.15 — Configure DCNM: SAN client, licensing, Device Manager (DCSAN Objective 3.1)

**Objective:** Confirm the switch is managed by DCNM/NDFC and licensed.

```bash
curl -sk -H "Authorization: $DCNM_TOK" "https://$DCNM/rest/control/fabrics" | jq -r '.[].fabricName'
```

```text
show license usage
```

**Expected result:** the SAN fabric listed in DCNM/NDFC and the switch's
license usage — DCNM SAN client and Device Manager are the GUI/analytics layer;
licensing gates the advanced features.

**Negative test:** query DCNM for a fabric the switch was never added to; it is
absent — DCNM manages only discovered fabrics.

**Cleanup:** none (read-only).

### Lab 5.16 — Configure RBAC (DCSAN Objective 3.2)

**Objective:** Create a role limited to a VSAN and a network-operator user.

```text
config t
 role name san-oper
  rule 1 permit show
  vsan policy deny
   permit vsan 100
 username sanuser password C1sco123! role san-oper
end
show role name san-oper
```

**Expected result:** the role permitting read-only access scoped to VSAN 100 —
RBAC confines operators to specific VSANs and command sets.

**Negative test:** log in as `sanuser` and attempt a `config` command; it is
denied — the role permits only `show`.

**Cleanup:** `no username sanuser ; no role name san-oper`.

### Lab 5.17 — Configure Fibre Channel fabric security (DCSAN Objective 3.3)

**Objective:** Enable port security / FC-SP DHCHAP on an interface.

```text
config t
 feature fabric-binding
 fabric-binding database vsan 100
  swwn 20:00:00:0d:ec:aa:bb:cc domain 10
 fabric-binding activate vsan 100
end
show fabric-binding status
show port-security database vsan 100
```

**Expected result:** fabric binding active, permitting only the listed switch
WWN/domain to join VSAN 100 — preventing a rogue switch from merging into the
fabric.

**Negative test:** connect an unlisted switch; its ISL is isolated and a
fabric-binding violation is logged — the binding enforces membership.

**Cleanup:** `fabric-binding deactivate vsan 100 ; no feature fabric-binding`.

### Lab 5.18 — Describe slow-drain analysis (DCSAN Objective 3.4)

**Objective:** Read the counters that reveal a slow-drain device.

```text
show interface fc1/1 counters | include "credit|discard|timeout"
show process creditmon credit-loss-events
show system internal snmp credit-not-available
```

**Expected result:** `credit unavailable`/`txwait` and B2B credit-loss events
— a slow-drain host holds credits and back-pressures the fabric; these
counters localize it.

**Negative test:** a healthy port shows zero txwait and no credit loss; the
contrast is how you distinguish a slow drainer from a busy-but-healthy port.

**Cleanup:** `clear counters interface fc1/1` after recording.

### Lab 5.19 — Implement SAN telemetry streaming (DCSAN Objective 3.5)

**Objective:** Enable SAN Analytics/telemetry on an interface.

```text
config t
 feature analytics
 interface fc1/1
  analytics type fc-scsi
end
show analytics query "select all from fc-scsi.port"
```

**Expected result:** per-flow SCSI metrics (IOPS, ECT/DAL latency) streamed
from the ASIC — SAN Analytics feeds Nexus Dashboard SAN Insights for
flow-level visibility.

**Negative test:** query analytics on an interface where the feature is not
applied; the result is empty — telemetry streams only from instrumented ports.

**Cleanup:** `interface fc1/1 ; no analytics type fc-scsi ; no feature
analytics`.

### Lab 5.20 — Troubleshoot Fibre Channel domains and duplicate domain ID (DCSAN Objective 4.1)

**Objective:** Read the FC domain manager and detect a domain-ID conflict.

```text
show fcdomain domain-list vsan 100
show fcdomain vsan 100
```

**Expected result:** the principal switch and each switch's domain ID; a
healthy fabric has unique IDs — a duplicate causes a VSAN to segment.

**Negative test:** statically assign a domain ID already in use and reinitialize the
fabric; `show fcdomain` reports the VSAN `isolated` due to the conflict — the
symptom of duplicate domains.

**Cleanup:** restore the domain ID to `auto` / a unique value and reinitialize.

### Lab 5.21 — Troubleshoot zoning and zone merge failure (DCSAN Objective 4.2)

**Objective:** Diagnose an ISL isolated by a zone-merge conflict.

```text
show zone status vsan 100
show interface fc1/1 | include "isolated|down"
show zone analysis active vsan 100
```

**Expected result:** a `merge` failure reason and the isolated ISL — two
switches with conflicting zone definitions for the same zone name refuse to
merge, isolating the link.

**Negative test:** two fabrics with identical, non-conflicting zonesets merge
cleanly — the contrast confirms the failure is a *conflict*, not merely
different content.

**Cleanup:** reconcile the zonesets (import/overwrite) and re-enable the ISL.

### Lab 5.22 — Troubleshoot boot and upgrade issues (DCSAN Objective 4.3)

**Objective:** Recover boot variables and read upgrade history.

```text
show boot
dir bootflash: | include nxos
show install all status
```

**Expected result:** the boot images present on bootflash and the last install
status — a failed upgrade or a missing image is why a switch lands in
`loader>`.

**Negative test:** point `boot system` at an image not on bootflash and reload;
the switch fails to boot — the boot variable must reference a present, valid
image.

**Cleanup:** set boot variables to the correct present images and save.

## Lab Verification

Verification means every login stage was evidenced, both faults were
induced and diagnosed by ladder rather than by guessing, and zoning
exports cleanly. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Storage networking is losslessness engineered: FC's credits and fabric
services, zoning's default-deny, dual fabrics' shared-nothing, and the
NPV/NPIV edge that scales logins without scaling fabrics. FCoE brings
the same guarantees to Ethernet with PFC/ETS/DCBX, and NVMe over
Fabrics carries the model into the flash era. The chapter is DCCOR's
20% storage domain entire, and its lossless-Ethernet machinery is
prerequisite reading for the AI fabrics of Chapter 07.

- [ ] I can walk the login ladder with its evidence commands
- [ ] My lab's dual-fabric zoning followed alias + smart-zoning
      practice
- [ ] I can explain PFC/ETS/DCBX and predict the mismatch symptom
- [ ] I can position FC-NVMe, NVMe/TCP, and NVMe/RoCE by estate
