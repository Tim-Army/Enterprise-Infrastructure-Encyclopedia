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

In the emulator/simulator environment (MDS features in CML where
image access permits, otherwise the documented UCS emulator SAN):
build VSAN 10 as Fabric A — NPIV core, device aliases, smart zoning,
activated zoneset — and connect Chapter 04's SAN-boot vHBA WWPNs
through it. Prove each ladder stage with its show command, captured.
Break it twice: deactivate the zoneset and capture the host's view;
misspell a device alias in a new zone and find it with the fabric's
own tools. Repair both, then export the zoning configuration for
Chapter 06's automation.

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
