# Chapter 08: OT/ICS Associate Architecture, Sensors, and Asset Visibility

## Learning Objectives

- Explain why enterprise IT visibility techniques (Chapters 1–2) are
  insufficient, by themselves, for safe OT/ICS asset visibility.
- Describe the eyeInspect architecture and how OT sensors differ in role
  from the enterprise appliances covered earlier in this volume.
- Map the Purdue Enterprise Reference Architecture model to sensor
  placement decisions across IT/OT boundary, cell/area zone, and site
  levels.
- Identify common industrial protocols (Modbus, DNP3, EtherNet/IP,
  IEC 61850, S7comm, and others) and what passive deep packet inspection
  can and cannot determine about them.
- Apply OT-specific discovery and classification principles that respect
  availability and safety constraints unique to industrial environments.
- Plan an OT sensor deployment that integrates with, but does not
  disrupt, existing IT visibility architecture.

## Theory and Architecture

Chapters 1–7 covered the enterprise IT side of the Forescout Platform —
appliances observing SPAN/mirror feeds, active scanning, and
credentialed endpoint inspection built for Windows, Linux, and general
IT/IoT devices. Operational technology (OT) and industrial control system
(ICS) environments — manufacturing floors, utility substations, building
management systems, and process-control networks — have fundamentally
different constraints, and the platform addresses them through a
dedicated capability: **eyeInspect** (the OT/ICS-focused module
introduced in Chapter 1's licensing table). This chapter and Chapter 9
cover the OT/ICS-specific FSCA and FSCE certification tracks referenced in
[CERTIFICATION_BLUEPRINTS.md](../../../CERTIFICATION_BLUEPRINTS.md).

### Why OT/ICS visibility is a distinct discipline

Three properties of OT/ICS environments make the enterprise-IT approach
from earlier chapters unsafe or ineffective to apply unmodified:

- **Availability and safety take precedence over confidentiality.** A
  process-control network's primary requirement is that the physical
  process it controls keeps running safely; an active scan technique
  that is routine on an IT segment (Chapter 1) can crash a
  legacy programmable logic controller (PLC) or induce unexpected
  behavior in safety-instrumented systems. OT visibility is therefore
  built around **strictly passive** monitoring as the default posture,
  not an optional lighter-touch setting.
- **Long equipment lifecycles and legacy protocols.** OT assets commonly
  run for fifteen to thirty years, often on embedded operating systems
  or proprietary firmware never designed with modern security telemetry
  in mind, communicating over industrial protocols with no native
  authentication or encryption.
- **Different asset taxonomy and risk model.** An OT asset inventory
  needs to represent not just IP-connected devices but the
  process-control hierarchy itself — controllers, human-machine
  interfaces (HMIs), engineering workstations, remote terminal units
  (RTUs), and the physical process context those devices serve — because
  risk in OT is measured against process safety and availability impact,
  not only data confidentiality.

### The Purdue model and sensor placement

The **Purdue Enterprise Reference Architecture** (commonly just "the
Purdue model") remains the standard reference framework for reasoning
about OT network layers and where visibility and security controls
belong:

| Level | Description | Typical assets |
| --- | --- | --- |
| Level 5 / 4 | Enterprise IT and business systems | ERP, corporate IT, general enterprise Forescout appliances (Chapters 1–7) |
| Level 3.5 | Industrial DMZ | Historian replication, patch/AV relay, jump hosts — the boundary IT and OT visibility architectures typically meet |
| Level 3 | Site/operations management | MES, plant historians, domain controllers dedicated to OT |
| Level 2 | Area supervisory control | HMIs, SCADA servers, engineering workstations |
| Level 1 | Basic control | PLCs, RTUs, controllers |
| Level 0 | Physical process | Sensors, actuators, field instrumentation |

eyeInspect sensors are placed to observe traffic at and below the
Level 3/Level 2 boundary, and at the Industrial DMZ (Level 3.5), where
they can passively see supervisory and control-network traffic without
being inline with anything safety-critical. Sensor placement decisions
map directly to this model: a sensor monitoring Level 3.5 traffic sees
IT/OT boundary crossings (the traffic most relevant to segmentation and
intrusion detection use cases), while a sensor monitoring Level 2/1
traffic within a specific cell or area zone sees the process-control
protocol detail needed for deep asset visibility and process-anomaly
detection within that zone.

### eyeInspect sensor architecture

An eyeInspect deployment is architecturally similar in spirit to the
enterprise appliance model from Chapter 1 — a purpose-built monitoring
node consuming a mirrored traffic feed — but tuned specifically for OT:

- **Passive sensors.** Physical or virtual appliances connected to
  SPAN/mirror ports or taps within OT network segments, performing deep
  packet inspection of industrial protocols without transmitting any
  probing or scanning traffic onto the OT network by default.
- **Protocol dissection engines.** Purpose-built parsers for industrial
  protocols that extract not just source/destination and protocol type
  (as enterprise IT fingerprinting does) but process-relevant detail:
  PLC program upload/download events, function-code-level Modbus
  operations, IEC 61850 GOOSE/MMS message types, and similar
  protocol-specific semantics that a generic IT-focused sensor cannot
  parse.
- **Central management integration.** eyeInspect sensor data integrates
  with the broader Forescout platform (Console/Enterprise Manager) so OT
  asset visibility appears alongside IT asset visibility in a unified
  inventory view, while sensor deployment and protocol-specific
  configuration remain managed through eyeInspect's own management
  plane.
- **Air-gapped and segmented deployment support.** Because many OT
  environments are deliberately segmented or fully air-gapped from
  general enterprise IT networks, eyeInspect supports deployment
  topologies where sensor data is aggregated locally within the OT
  environment and forwarded to central management through a controlled,
  narrowly scoped path (often through the Industrial DMZ) rather than
  requiring direct connectivity from every sensor to enterprise IT.

### Industrial protocols and what passive DPI reveals

| Protocol | Common use | What passive DPI typically reveals |
| --- | --- | --- |
| Modbus (TCP/RTU) | Widely used, simple request/response protocol across many PLC vendors | Function codes (read/write coil, register), register addresses accessed, device role inference from traffic pattern |
| DNP3 | Utility/SCADA, especially electric and water | Object types exchanged, unsolicited response patterns, master/outstation relationships |
| EtherNet/IP (CIP) | Rockwell Automation and broader CIP-based environments | Device identity objects, I/O connection establishment, explicit messaging service codes |
| IEC 61850 (GOOSE/MMS/SV) | Electric substation automation | GOOSE message publishers/subscribers, MMS service requests, logical-node-level detail in well-formed networks |
| S7comm / S7comm+ | Siemens PLC families | Program upload/download activity, PLC start/stop commands, block-level operations |
| BACnet | Building automation | Device object discovery, read/write property operations |

Passive DPI reveals protocol-level *behavior* — what operations are
occurring, between which endpoints, at what frequency — without altering
or interrupting that traffic. It does not, by itself, confirm whether an
observed operation is authorized in a business-process sense (a
legitimate engineer pushing a scheduled PLC program update looks
identical at the protocol level to an unauthorized one); that
authorization context has to come from correlating sensor data with
change-management records, engineering workstation identity, and
timing expectations — the asset-curation and threat-detection discipline
covered in depth in Chapter 9.

## Design Considerations

- **Passive-only as the default, not the exception.** Unlike enterprise
  IT deployments where active scanning is a normal, tunable enhancement
  (Chapter 1), OT deployments should treat active techniques as an
  explicit, individually risk-assessed exception requiring plant
  engineering sign-off — never a default setting.
- **Sensor placement by zone, not by convenience.** Place sensors
  according to the Purdue-model zone boundaries that matter for the
  organization's risk model (cell/area zone boundaries, the Industrial
  DMZ) rather than wherever a SPAN port happens to already exist, since
  incorrect placement can create a false sense of coverage.
- **Bandwidth and mirror capacity in legacy switch infrastructure.**
  Older OT-segment switches may have limited or no SPAN capability;
  plan for tap hardware or a phased switch-refresh project rather than
  assuming SPAN is universally available the way it typically is in
  modern enterprise IT infrastructure.
- **Segmentation and connectivity of the sensor's management path.**
  Design how sensor data reaches central management without creating a
  new, insufficiently controlled path between the OT environment and
  enterprise IT — the sensor's own management connectivity must not
  become the segmentation violation the broader security program is
  trying to prevent.
- **Change-management alignment.** OT environments typically have
  formal, safety-driven change-management processes already in place
  (planned maintenance windows, engineering change orders); design asset
  visibility and any future control capability (Chapter 9) to integrate
  with those existing processes rather than introducing a parallel,
  IT-style change process unfamiliar to plant operations staff.
- **Stakeholder alignment between IT security and OT/plant engineering.**
  OT visibility programs succeed or fail on this relationship; involve
  plant engineering and safety stakeholders from the sensor-placement
  planning stage, not only after deployment, since they hold the
  authoritative knowledge of which network segments are safety-critical.

## Implementation and Automation

1. **Conduct a Purdue-model network survey** of the target OT
   environment, documenting existing zone boundaries, known switch
   SPAN/tap capability, and the Industrial DMZ's current architecture (or
   the plan to establish one if it does not yet exist).
2. **Prioritize sensor placement** at the Industrial DMZ and at
   cell/area zone boundaries identified as highest risk or highest asset
   criticality, rather than attempting full simultaneous coverage across
   every zone in an initial phase.
3. **Deploy sensors passively**, connecting monitor interfaces to
   SPAN/mirror sessions or taps exactly as in Chapter 1's enterprise
   pattern, but with an explicit verification step confirming no sensor
   interface is inadvertently configured to transmit onto the monitored
   segment.
4. **Validate protocol dissection** against a small set of known assets
   per protocol in scope (a known PLC, a known HMI) before broadening
   sensor scope, confirming the sensor correctly identifies device
   role and protocol detail for assets whose ground truth is already
   known.
5. **Integrate sensor data into the unified inventory**, confirming OT
   assets appear in the Console alongside IT assets with clearly
   distinguishable OT-specific properties (protocol role, vendor/model
   where derivable, Purdue level).
6. **Establish a baseline observation period** (commonly longer than the
   enterprise IT baseline in Chapter 1 — OT traffic patterns often
   follow production shift schedules and periodic maintenance cycles
   that a short window will not capture) before any classification or
   future policy work depends on the data being representative.
7. **Document the sensor deployment's Purdue-level coverage map** as a
   living artifact, so future sensor-placement decisions (Chapter 9)
   build on an explicit record of what is and is not currently visible.

## Validation and Troubleshooting

- **No traffic observed on a newly connected OT sensor.** Apply the same
  first checks as Chapter 1's enterprise SPAN troubleshooting (switch
  SPAN session active, correct source, monitor interface up), but also
  confirm the OT switch itself supports and is licensed for SPAN/mirror
  functionality — a nontrivial share of legacy OT switching hardware does
  not.
- **A known device is visible but its protocol detail is not being
  dissected.** Confirm the specific protocol is within the sensor's
  licensed/enabled dissection scope, and check for a non-standard port or
  encapsulation the device uses that the dissection engine may not be
  configured to recognize by default.
- **Sensor data is not appearing in the unified Console inventory.**
  Check the sensor-to-central-management integration path first (the
  air-gapped/segmented forwarding architecture described above is a
  common source of connectivity gaps distinct from the sensor's own
  local visibility, which can be healthy even when forwarding is broken).
- **Asset count or protocol activity looks inconsistent with known plant
  operations.** Cross-check against the production shift schedule and
  maintenance calendar before assuming a sensor defect — OT traffic
  volume and protocol mix legitimately varies by shift and by planned
  maintenance activity far more than typical enterprise IT traffic does.
- **Plant engineering reports a concern about sensor impact.** Treat this
  as a priority investigation regardless of technical plausibility;
  confirm from packet capture (where safe to obtain) or sensor
  configuration review that the sensor truly is operating passively, and
  document the finding back to the stakeholder, since maintaining OT
  engineering trust is operationally as important as the technical
  finding itself.

## Security and Best Practices

- Default every OT sensor deployment to strictly passive operation, and
  require explicit, documented, engineering-approved sign-off before
  enabling any active technique in an OT segment.
- Segment and control the sensor's own management-plane connectivity
  with the same rigor applied to any other IT/OT boundary crossing,
  including its data-forwarding path to central management.
- Treat OT asset inventory data (device models, firmware versions,
  network topology) as sensitive in its own right — it is
  reconnaissance-grade information about critical infrastructure, and
  access to it should be scoped as tightly as the RBAC guidance in
  Chapter 4.
- Coordinate any sensor deployment or configuration change through the
  same change-management process governing the OT environment itself,
  including advance notice to plant operations regardless of how low-risk
  the change appears from a pure IT perspective.
- Maintain a clear, documented boundary between visibility (this
  chapter) and any control capability (Chapter 9) — do not enable
  OT control actions incidentally as a side effect of a visibility
  deployment; treat that as a distinct, separately risk-assessed decision.
- Recognize that many industrial protocols carry no native
  authentication, meaning passive visibility of an operation does not by
  itself confirm the operation was authorized — corroborate with
  change-management and identity context before treating an observation
  as either benign or malicious.

## References and Knowledge Checks

**References**

- Forescout Technologies eyeInspect (OT/ICS) architecture and sensor
  deployment documentation for the current release aligned with this
  volume's 8.5.x platform baseline.
- [SOFTWARE_VERSIONS.md](../../../SOFTWARE_VERSIONS.md) — dated platform
  baseline for this volume.
- Purdue Enterprise Reference Architecture (PERA) — the industry-standard
  reference model for ICS network layering used throughout this chapter
  and Chapter 9.
- [CERTIFICATION_BLUEPRINTS.md](../../../CERTIFICATION_BLUEPRINTS.md) —
  FSCA: OT/ICS and FSCE: OT/ICS blueprint domain mapping for this volume.
- Chapter 1 of this volume for the enterprise appliance and passive
  discovery architecture this chapter adapts for OT/ICS.

**Knowledge Checks**

1. Why is passive-only monitoring the default posture in OT/ICS
   environments rather than an optional lighter-touch setting, as active
   scanning is in enterprise IT?
2. Map eyeInspect sensor placement to at least two Purdue model levels
   and explain what each placement is best suited to reveal.
3. Choose two industrial protocols from this chapter's table and
   describe what passive DPI reveals about each, and one limitation of
   that visibility.
4. Why does an OT baseline observation period typically need to be
   longer than the enterprise IT baseline from Chapter 1?
5. Why must passive protocol-level observation be corroborated with
   change-management and identity context before an operation can be
   judged authorized or unauthorized?

## Hands-On Lab

**Objective.** Plan and validate a passive OT sensor placement against a
simulated Purdue-model network segment, and confirm protocol visibility
without any active technique.

**Prerequisites**

- A lab or trial eyeInspect sensor (physical or virtual), or a general
  network-analysis tool substituting for it if a licensed lab sensor is
  unavailable — see the note in step 2 below for how to adapt the lab
  accordingly.
- A simulated OT segment: at minimum a PLC simulator or an industrial
  protocol traffic generator capable of producing Modbus TCP traffic
  (widely available as open lab/training tools), connected to a lab
  switch capable of a SPAN/mirror session.
- A documented (even if simplified) Purdue-model diagram of the lab
  topology showing where the simulated PLC, an HMI or engineering
  workstation simulator, and the sensor's monitor point sit.

**Procedure**

1. Draw or annotate the lab's Purdue-model diagram, labeling the
   simulated PLC as Level 1, the HMI/engineering workstation simulator as
   Level 2, and the sensor's planned monitor point at the boundary
   between them.
2. Configure a SPAN session on the lab switch sourcing the traffic
   between the PLC simulator and the HMI/engineering workstation
   simulator, destined to the sensor's monitor interface. If a licensed
   eyeInspect sensor is unavailable, substitute a general packet-capture
   tool at the same monitor point and manually inspect Modbus function
   codes in the capture as a substitute for automated dissection.
3. Generate representative Modbus traffic from the simulator (read
   holding registers, write single coil operations) between the two
   simulated endpoints.
4. Confirm the sensor (or packet capture) observes the traffic and
   correctly identifies the protocol and, where the tool supports it, the
   specific function codes used.
5. Confirm the sensor's monitor interface is configured receive-only and
   review its configuration to verify no active probing capability is
   enabled.
6. Document the observed asset behavior (which endpoint issues read
   operations, which responds, at what approximate frequency) as a
   miniature asset-behavior baseline.
7. **Negative test.** Disconnect or shut down the SPAN destination
   interface on the switch and confirm the sensor (or capture tool)
   immediately loses visibility of the simulated PLC traffic, with no
   compensating active technique attempting to reach the PLC directly —
   demonstrating that OT visibility, correctly configured, degrades to
   silence rather than falling back to an active technique when passive
   delivery is interrupted. Re-enable the SPAN session afterward and
   confirm visibility resumes.

**Expected Results**

- The Purdue-model diagram correctly places the simulated assets and the
  sensor's monitor point.
- The sensor or capture tool correctly observes and identifies Modbus
  traffic and function-code-level detail between the simulated PLC and
  HMI/engineering workstation.
- The monitor interface is confirmed passive/receive-only.
- The negative test confirms visibility loss on SPAN interruption with no
  active fallback behavior, and confirms recovery once SPAN is restored.

**Cleanup**

- Remove the lab SPAN session if the switch interfaces are needed
  elsewhere (`no monitor session <ID>` on Cisco IOS-style switches).
- Stop the PLC/protocol traffic simulator if it will not be reused in
  Chapter 9's lab.
- Retain the annotated Purdue-model diagram; Chapter 9's lab builds on
  it.

## Summary and Completion Checklist

This chapter established why OT/ICS asset visibility is a distinct
discipline from enterprise IT visibility (Chapters 1–2), centered on the
Purdue Enterprise Reference Architecture as the framework for reasoning
about sensor placement, the eyeInspect sensor architecture and its
strictly passive default posture, and what passive deep packet inspection
of industrial protocols (Modbus, DNP3, EtherNet/IP, IEC 61850, S7comm,
BACnet, and others) can and cannot reveal about process-control
operations. Chapter 9 builds on this visibility foundation to cover
OT/ICS deployment design at expert depth, asset curation, and
OT-specific troubleshooting.

**Completion checklist**

- [ ] Can explain why OT/ICS visibility defaults to passive-only, unlike
      enterprise IT's tunable active-scanning posture.
- [ ] Can map sensor placement decisions to Purdue model levels and
      explain the visibility trade-off at each.
- [ ] Can describe what passive DPI reveals (and does not reveal) for at
      least three industrial protocols.
- [ ] Completed the hands-on lab, including the Purdue-model diagram and
      the passive-visibility negative test.
- [ ] Understands why passive observation alone cannot confirm
      authorization without change-management and identity correlation.
