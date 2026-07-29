# Chapter 09: OT/ICS Expert Design, Deployment, Curation, and Troubleshooting

![Lab topology for this chapter: a second simulated cell/area zone extends the prior chapter's single zone, each independently visible through its own SPAN session and sensor; a curation pass compares sensor-observed assets against a manually maintained asset register, producing at least one documented discrepancy finding. A behavioral baseline defines one zone as reads-only under normal operation, and a deliberate write/program-download operation is confirmed distinguishable from that baseline. As a negative test, the anomalous operation is correlated against a change ticket that deliberately does not exist yet, correctly escalating as unapproved; creating a matching change record after the fact causes the same operation to now correlate as approved.](../../../diagrams/volume-015-forescout-platform-certifications/chapter-09-ot-two-zone-curation-baseline-topology.svg)

*Figure 9-1. Topology used throughout this chapter's Hands-On Lab: a two-zone OT visibility extension with an asset-register curation pass and a behavioral baseline, tested against change-ticket correlation.*

## Learning Objectives

- Design a multi-site eyeInspect sensor topology sized to zone-level
  asset count and protocol mix rather than generic host-count heuristics.
- Apply asset curation practices that maintain OT inventory accuracy and
  trustworthiness over the life of a deployment.
- Design OT-appropriate threat detection logic that respects the
  authorization-context limitation established in [Chapter 8](08-ot-ics-associate-architecture-sensors-and-asset-visibility.md).
- Plan a security-cleared, staged approach to any OT control capability,
  distinct from and more conservative than the enterprise eyeControl
  staging pattern in [Chapter 3](03-clarification-compliance-and-control-policies.md).
- Troubleshoot OT sensor and dissection issues using an OT-adapted version
  of the layered diagnostic model from [Chapter 6](06-advanced-troubleshooting-performance-and-resilience.md).
- Synthesize Chapters 8–9 into a complete OT/ICS visibility and
  governance design, mapped to the FSCA: OT/ICS and FSCE: OT/ICS
  certification blueprint domains.

## Theory and Architecture

[Chapter 8](08-ot-ics-associate-architecture-sensors-and-asset-visibility.md) established the OT/ICS visibility foundation: the Purdue model,
passive-only eyeInspect sensor architecture, and what industrial protocol
dissection reveals. This chapter moves from associate-level visibility to
expert-level deployment design, ongoing asset curation, threat detection,
and the more conservative path to any OT control capability — the
material aligned to the FSCE: OT/ICS blueprint domain referenced in
[CERTIFICATION_BLUEPRINTS.md](../../../CERTIFICATION_BLUEPRINTS.md).

### Multi-site sensor topology design

A mature OT/ICS deployment spans multiple sites (plants, substations,
facilities), each with its own zone structure. Expert-level design
extends [Chapter 8](08-ot-ics-associate-architecture-sensors-and-asset-visibility.md)'s single-zone placement principles into a topology
decision:

- **Zone-scoped sensors, site-scoped aggregation.** Each cell/area zone
  or Industrial DMZ segment identified in the [Chapter 8](08-ot-ics-associate-architecture-sensors-and-asset-visibility.md) coverage map gets
  its own sensor (or shared sensor scoped to that zone's traffic only),
  with site-level aggregation consolidating multiple zone sensors' data
  for local site visibility before it is forwarded further.
- **Sizing by zone asset density and protocol complexity, not raw
  bandwidth.** As with enterprise appliance sizing in [Chapter 1](01-platform-architecture-installation-and-deployment-planning.md), OT
  sensor capacity planning is driven by the number of distinct devices
  and control-relationship pairs a zone's protocol traffic represents,
  and by how protocol-complex that traffic is to dissect (a zone rich in
  IEC 61850 GOOSE traffic, for example, is more dissection-intensive per
  packet than a simple point-to-point Modbus link).
- **Resilient forwarding across constrained links.** Site-to-central
  forwarding paths in industrial environments are sometimes low-bandwidth
  or intermittently available (a remote substation on a constrained WAN
  link, for example); design forwarding to buffer and resume rather than
  drop data during a transient link outage, and size local retention at
  each site to cover the expected outage duration.
- **Standardized zone naming and topology metadata.** Adopt a consistent
  site/zone naming convention across the whole topology from the first
  multi-site deployment, since retrofitting naming consistency across a
  large sensor estate later is disproportionately expensive compared to
  establishing it up front.

### Asset curation

**Asset curation** is the ongoing discipline of keeping OT asset
inventory accurate, deduplicated, and trustworthy — distinct from the
one-time baseline validation covered in [Chapter 8](08-ot-ics-associate-architecture-sensors-and-asset-visibility.md). Curation matters more
in OT than in enterprise IT because OT assets are long-lived, rarely
replaced wholesale, and often only partially identifiable from network
traffic alone (a passively observed PLC may reveal its protocol role
clearly while its exact model or firmware revision remains uncertain
without corroborating engineering documentation). Core curation
activities:

- **Merging and deduplication.** Resolving cases where the same physical
  asset appears as multiple inventory records (common after a device's
  IP address changes, or when it is observed from two different sensor
  vantage points before correlation logic merges the records).
- **Enrichment from engineering sources.** Supplementing passively
  derived properties with data from engineering documentation, asset
  registers, or a plant historian/CMMS system where such an integration
  exists — closing the gap between "protocol role observed" and
  "specific make, model, and firmware version confirmed."
- **Confidence and staleness tracking.** Distinguishing an asset record
  recently corroborated by fresh traffic from one that has not been
  observed in an extended period (a device that fell off the network
  during a planned outage, versus one that may have been decommissioned
  without the inventory being updated).
- **Periodic curation review.** Scheduling a recurring review (aligned to
  a plant's maintenance or shutdown calendar where practical) to
  reconcile the inventory against known engineering changes, rather than
  treating the OT inventory as self-maintaining the way well-instrumented
  enterprise IT inventory largely is.

### Threat detection in OT/ICS

Building on [Chapter 8](08-ot-ics-associate-architecture-sensors-and-asset-visibility.md)'s authorization-context limitation, expert-level OT
threat detection combines passive protocol observation with additional
context to distinguish legitimate operations from anomalous ones:

- **Behavioral baselining.** Establishing what "normal" looks like per
  zone — which endpoints communicate, using which function codes, at
  what frequency and during what shift/maintenance windows — over the
  extended observation period recommended in [Chapter 8](08-ot-ics-associate-architecture-sensors-and-asset-visibility.md), then alerting on
  material deviation.
- **Known-bad protocol behavior detection.** Independent of baselining,
  detecting protocol operations understood to be inherently high-risk
  regardless of baseline (an unexpected PLC stop command, a firmware
  upload to a controller outside a declared maintenance window).
- **Cross-referencing change-management data.** Where an integration to
  the plant's change-management or maintenance-scheduling system exists
  (conceptually similar to the eyeExtend ITSM integration pattern in
  [Chapter 5](05-advanced-policy-integrations-and-business-outcomes.md)), correlating an observed sensitive operation against a
  corresponding approved change record before escalating it as anomalous.
- **IT/OT boundary-crossing detection.** Applying particular scrutiny to
  any traffic crossing the Industrial DMZ in either direction, since the
  IT/OT boundary is both the most architecturally significant
  segmentation point and the most common path for both legitimate
  remote-support access and OT-targeted intrusions.

### The conservative path to OT control capability

Enterprise eyeControl ([Chapter 3](03-clarification-compliance-and-control-policies.md)) stages control actions from monitor
mode to live enforcement over a period of weeks. OT/ICS control
capability — where it is used at all — requires a materially more
conservative approach, because an incorrect control action in OT can have
physical safety consequences, not only an access-disruption consequence:

- **Visibility-only as the durable default**, not merely the starting
  point. Many mature OT/ICS deployments remain visibility-only
  indefinitely by design, using the platform for asset inventory, threat
  detection, and alerting while routing any actual response through
  existing OT change-management and incident-response processes rather
  than automated network action.
- **Extended, engineering-supervised monitor mode** where control
  capability is pursued at all, run for a period measured in months
  rather than weeks, with plant engineering directly reviewing simulated
  actions before any enforcement is considered.
- **Narrow, low-risk action scope first.** If enforcement is ever
  enabled, start with the least physically consequential action
  available (alerting/notification escalation, or segmentation actions
  confined to the IT/OT boundary rather than within a safety-critical
  cell) rather than a broad quarantine or blocking action against
  control-network traffic itself.
- **Joint IT security and OT engineering sign-off** as a mandatory gate
  before any OT enforcement action goes live, formalized the same way a
  safety-instrumented-system change would be, not treated as a standard
  IT change-management approval.

## Design Considerations

- **Topology standardization before scale.** Establish naming, zone
  taxonomy, and sizing conventions during the first multi-site rollout;
  the cost of inconsistency compounds with every additional site added
  under a different convention.
- **Curation ownership.** Assign explicit ownership for OT asset curation
  — a joint responsibility between IT security/platform administration
  and plant engineering — since neither side alone typically holds both
  the technical inventory access and the engineering ground truth needed
  to curate effectively.
- **Alert fatigue vs. detection sensitivity.** Calibrate behavioral
  baselining sensitivity deliberately; an OT threat-detection program
  that generates high false-positive volume quickly loses plant
  operations trust and gets tuned down or ignored, which is a worse
  long-term outcome than a slightly less sensitive but sustainably
  monitored baseline.
- **Control capability as an explicit, revisitable decision.** Treat
  "visibility-only, indefinitely" as a legitimate, deliberate program
  outcome rather than an unfinished maturity stage every deployment must
  eventually graduate past; revisit the decision periodically based on
  actual risk and organizational readiness rather than defaulting toward
  control capability by inertia.
- **Retention and resilience for constrained-link sites.** Size local
  data retention at remote or link-constrained sites to the realistic
  outage duration the WAN link experiences, informed by the site's actual
  historical link-reliability data rather than an assumed enterprise-grade
  connectivity baseline.
- **Cross-functional incident response.** Design OT incident response
  procedures jointly with plant engineering and safety stakeholders
  before an incident occurs, since an IT-only incident-response runbook
  applied to an OT-related event risks a response action that itself
  introduces safety or availability risk.

## Implementation and Automation

1. **Build the multi-site zone/sensor topology map**, extending the
   single-zone [Chapter 8](08-ot-ics-associate-architecture-sensors-and-asset-visibility.md) coverage map to every site and zone in
   scope, with standardized naming applied from the start.
2. **Deploy and validate sensors zone by zone**, following [Chapter 8](08-ot-ics-associate-architecture-sensors-and-asset-visibility.md)'s
   passive-deployment and protocol-dissection validation steps at each
   new zone before expanding further.
3. **Establish site-level aggregation and resilient forwarding**,
   testing behavior under a simulated link interruption (see the Chapter
   6 resilience-testing pattern, applied here to OT forwarding paths)
   before relying on it operationally.
4. **Stand up the asset curation workflow.** Define the recurring review
   cadence, the enrichment data sources (engineering documentation,
   asset register, CMMS integration where available), and the specific
   staleness threshold that flags a record for review.
5. **Build behavioral baselines per zone** over the extended observation
   period, then author threat-detection alerting rules referencing that
   baseline plus the known-bad-behavior detections described above. A
   representative alerting rule in outline form:

   ```text
   RULE "Unscheduled PLC Program Change"
     IF  Protocol Operation = "Program Download"
     AND Zone = "Line 3 Cell Controllers"
     AND Change Ticket Reference (via integration) = NOT FOUND
     THEN action: escalate to OT-SOC with high priority
          action: notify plant engineering on-call
   ```

6. **Integrate change-management correlation** where a maintenance or
   change-tracking system is available, so alerting rules like the one
   above can distinguish approved from unapproved sensitive operations
   automatically rather than requiring manual lookup for every alert.
7. **If pursuing control capability, formally document the joint
   sign-off gate** (IT security and OT engineering) as a required step in
   the staged rollout, and record the specific narrow action scope
   approved for initial enforcement.
8. **Produce the OT/ICS design synthesis document** covering topology,
   curation workflow, threat-detection logic, and the control-capability
   decision (with rationale, whether that decision is "visibility-only"
   or a scoped enforcement plan) as the chapter's capstone deliverable.

## Validation and Troubleshooting

- **Sensor topology has a coverage gap discovered after deployment.**
  Cross-check the actual deployed sensor map against the documented
  zone/topology plan from [Chapter 8](08-ot-ics-associate-architecture-sensors-and-asset-visibility.md) and this chapter; coverage gaps
  most often trace back to a zone that was deprioritized in an earlier
  phase and never revisited, not to a technical sensor failure.
- **Asset curation review surfaces many stale or duplicate records.**
  This is expected in a first curation pass on an established
  deployment and is not itself a defect — treat it as the baseline the
  recurring curation cadence is meant to prevent from recurring, and
  investigate the merge/deduplication logic only if the same duplicates
  reappear after being resolved once.
- **Behavioral baseline alerting produces high false-positive volume
  after a plant process change.** Confirm whether the underlying process
  itself changed (a genuine new legitimate pattern) before assuming a
  detection-logic defect; OT baselines need deliberate re-baselining
  after a known, approved process or equipment change, not only after an
  extended natural drift period.
- **Change-management correlation fails to match an approved change to
  an observed operation.** Check timing-window tolerance and identifier
  matching logic first — a mismatch between the change record's approved
  window and the actual execution time (common when maintenance runs
  early or late) is a more frequent cause than a broken integration.
- **A resilient-forwarding site fails to catch up after a prolonged link
  outage.** Confirm local retention at that site did not exceed its
  configured buffer during the outage; an outage longer than the
  provisioned retention window results in a genuine, unrecoverable data
  gap that should be documented as such rather than assumed to be a
  forwarding defect.

## Security and Best Practices

- Apply the same least-privilege and audit-logging discipline from
  Chapters 2, 4, and 7 to OT asset curation access and to any
  change-management integration credential, recognizing that OT
  inventory and topology data are themselves sensitive, reconnaissance-
  relevant assets.
- Keep the control-capability decision explicit, documented, and jointly
  owned by IT security and OT engineering leadership — an undocumented
  drift from "visibility-only" toward informal control usage is a
  governance failure to guard against specifically.
- Extend incident-response and tabletop-exercise programs to explicitly
  cover OT/ICS scenarios, with plant engineering and safety stakeholders
  as required participants, not observers.
- Treat any narrow OT enforcement action, once approved, with the same
  rollback-readiness discipline as [Chapter 3](03-clarification-compliance-and-control-policies.md)'s enterprise control
  policies, but scaled to OT's higher consequence tolerance — the
  rollback procedure itself should be reviewed and approved by plant
  engineering before the enforcement action is enabled.
- Periodically reassess whether the organization's OT threat landscape
  and regulatory obligations (sector-specific requirements for utilities,
  manufacturing, or critical infrastructure operators, as applicable)
  still match the deployment's current visibility and control posture,
  since both the threat landscape and regulatory expectations evolve
  independently of the platform itself.

## References and Knowledge Checks

**References**

- [Forescout Technologies eyeInspect advanced deployment, asset curation,
  and threat detection documentation for the current release aligned
  with this volume's 8.5.x platform baseline.](https://www.forescout.com/product/eyeinspect/)
- [SOFTWARE_VERSIONS.md](../../../SOFTWARE_VERSIONS.md) — dated platform
  baseline for this volume.
- [Chapter 8](08-ot-ics-associate-architecture-sensors-and-asset-visibility.md) of this volume for the Purdue model, sensor architecture, and
  protocol dissection foundation this chapter builds on.
- [CERTIFICATION_BLUEPRINTS.md](../../../CERTIFICATION_BLUEPRINTS.md) —
  FSCA: OT/ICS and FSCE: OT/ICS blueprint domain mapping for this volume.
- [Forescout Technologies certification and training catalog (official
  source for current FSCA: OT/ICS and FSCE: OT/ICS blueprint domains and
  exam registration).](https://www.forescout.com/support-hub/training/)

**Knowledge Checks**

1. Why does multi-site OT sensor sizing depend on zone asset density and
   protocol complexity rather than raw bandwidth, echoing but adapting
   the enterprise sizing principle from [Chapter 1](01-platform-architecture-installation-and-deployment-planning.md)?
2. What is asset curation, and why does OT inventory need an ongoing
   curation discipline that mature enterprise IT inventory largely does
   not?
3. Describe two complementary approaches to OT threat detection and the
   authorization-context gap each helps close.
4. Why does this chapter treat "visibility-only, indefinitely" as a
   legitimate program outcome rather than an incomplete maturity stage?
5. What must be true — organizationally and procedurally — before any
   narrow OT control action should be enabled, according to this
   chapter's conservative staging model?

## Hands-On Lab

This chapter carries a topic-level walkthrough lab for **each theme of expert OT/ICS work
with eyeInspect** — multi-site sensor topology design, asset curation, OT threat detection,
and the conservative path to OT control — mapped to the FSCE: OT/ICS track. It opens with a
**Design Exercise** (the expert deliverable) and follows with Command Center walkthroughs.
Each ends **`**Lab verified by:** *pending*`** until a human runs it.

**Shared prerequisites for Labs 9.1–9.4** — a multi-sensor eyeInspect deployment reporting
to a Command Center, a lab OT segment or replayed captures, and (for Lab 9.4) awareness of
the IT/OT boundary where the enterprise Forescout platform can enforce. **Cost:** none
beyond lab resources. **Safety:** all steps are passive; stage any control only at the
IT/OT boundary, never on the process network.

### Lab 9.1 — Design Exercise: multi-site OT sensor topology (Topic: OT design)

**Objective:** Produce a defensible multi-site OT monitoring design, not a config dump.

> **Scenario.** A utility runs 1 central SOC and 12 remote substations/plants, each with
> its own Level 0–2 process network and a Level 3 site network, connected back to a
> corporate IT/OT DMZ. They need full OT visibility, threat detection, and eventual
> boundary control — with zero disruption to the process network.

Work through and **write down**:

1. **Sensor placement per site** — which SPAN/TAP points at Levels 1, 2, and 3, and a
   boundary sensor at the IT/OT DMZ (Level 3.5).
2. **Aggregation** — one central Command Center vs. regional collectors; bandwidth for
   sensor-to-CC telemetry over the WAN.
3. **Redundancy** — sensor and CC resilience; what visibility is lost if a site link drops.
4. **Data handling** — where captures/alerts live, and OT data-sovereignty constraints.
5. **Control boundary** — where enforcement is *allowed* (the IT/OT DMZ via the enterprise
   platform) and where it is forbidden (the process network).

**Expected result:** a written design naming per-site sensor placement, aggregation
topology, redundancy, and an explicit control boundary — the FSCE: OT/ICS deliverable, where
the safety-driven *why* (never disrupt the process) governs every choice.

**Negative test:** design OT control actions on the Level 1 process network for "faster
response"; an errant block could stop a physical process — the expert design confines
enforcement to the IT/OT boundary.

**Cleanup:** none (design artifact).

### Lab 9.2 — Asset curation (Topic: Asset curation)

**Objective:** Refine the passive inventory into a trustworthy asset database.

```text
# Command Center: Asset Inventory —
#   - merge duplicate asset entries (same device seen via multiple addresses/sensors)
#   - correct/enrich roles and labels (PLC vs HMI vs engineering workstation)
#   - assign assets to the correct site/zone and Purdue level
#   - flag unknown/unexpected assets for investigation
```

**Expected result:** a curated inventory with deduplicated, correctly labeled, zone-assigned
assets — curation turns raw passive discovery into an authoritative asset database that
detection and reporting can trust; an inventory that has not been curated produces noisy, low-confidence
alerts.

**Negative test:** run threat detection on an inventory that has not been curated, full of duplicates and
mislabels; every benign change looks anomalous and analysts drown in false positives —
curation is the prerequisite for meaningful detection.

**Cleanup:** none (keep the curation; it is the intended state).

### Lab 9.3 — OT threat detection (Topic: Threat detection)

**Objective:** Baseline normal OT behavior and alert on a meaningful deviation.

```text
# Command Center: enable behavioral baselining and relevant checks/policies, then
#   observe alerts for, e.g.:
#   - a new/unauthorized asset appearing on the process network
#   - an engineering action (PLC program upload/download) outside a maintenance window
#   - an unexpected communication (a new master talking to a controller)
```

**Expected result:** eyeInspect raises prioritized alerts on deviations from the OT baseline
— a new device, an out-of-window controller program change, an unexpected master/slave
relationship — the changes that matter in an environment where "normal" is far more static
than IT.

**Negative test:** port IT alerting thresholds directly into OT; OT's low-variance traffic
makes IT-tuned rules either miss subtle control-plane attacks or flood on benign polling —
detection must be tuned to the OT baseline.

**Cleanup:** revert lab-only checks; keep production baselines.

### Lab 9.4 — Staged path to OT control (Topic: OT control)

**Objective:** Plan boundary enforcement without touching the process network.

```text
# Design + (where safe) stage at the IT/OT boundary only:
#   1. Visibility  -> confirmed (Chapters 08, 9.2)
#   2. Detection   -> confirmed (9.3)
#   3. Alert-to-action -> integrate eyeInspect alerts to the SOC/enterprise Forescout
#      platform so the IT/OT DMZ can quarantine a compromised IT-side host.
#   Do NOT configure active control on Level 0-2 process assets.
```

**Expected result:** a staged plan where control is exercised only at the IT/OT boundary —
e.g. the enterprise Forescout platform quarantines a compromised jump host in the DMZ on an
eyeInspect alert — while the process network remains observe-only; OT control is deliberately
conservative because availability and safety outrank containment.

**Negative test:** deploy automated blocking onto the process network the way you would in
IT; a false positive can halt production or trip a safety system — the staged, boundary-only
approach is the OT-appropriate control model.

**Cleanup:** none (design/staging artifact; no process-network control configured).

## Lab Verification

Complete this sign-off once the lab has been run end to end, including the
negative test. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

This chapter completed the volume's OT/ICS track by extending [Chapter 8](08-ot-ics-associate-architecture-sensors-and-asset-visibility.md)'s
visibility foundation into expert-level multi-site sensor topology
design, ongoing asset curation as a distinct operational discipline from
one-time baselining, threat-detection logic that closes the
authorization-context gap through behavioral baselining and
change-management correlation, and a deliberately conservative,
engineering-supervised path to any OT control capability — treating
visibility-only as a legitimate, durable program outcome rather than an
incomplete stage. Together with [Chapter 7](07-expert-automation-api-governance-and-capstone.md)'s enterprise capstone, this
chapter closes the volume's coverage of the FSCA, FSCP, FSCE, FSCA:
OT/ICS, and FSCE: OT/ICS certification blueprint domains.

**Completion checklist**

- [ ] Can design a multi-site sensor topology sized to zone asset density
      and protocol complexity.
- [ ] Can describe the asset curation workflow and why OT inventory
      requires it on an ongoing basis.
- [ ] Can design threat-detection logic combining behavioral baselining
      and change-management correlation.
- [ ] Completed the hands-on lab, including the two-zone extension, the
      curation pass, and the change-correlation negative test.
- [ ] Understands why OT control-capability staging is deliberately more
      conservative than the enterprise eyeControl pattern in [Chapter 3](03-clarification-compliance-and-control-policies.md),
      and can articulate the joint sign-off gate this chapter requires.
