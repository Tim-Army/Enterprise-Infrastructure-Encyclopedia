# Chapter 09: OT/ICS Expert Design, Deployment, Curation, and Troubleshooting

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

- Forescout Technologies eyeInspect advanced deployment, asset curation,
  and threat detection documentation for the current release aligned
  with this volume's 8.5.x platform baseline.
- [SOFTWARE_VERSIONS.md](../../../SOFTWARE_VERSIONS.md) — dated platform
  baseline for this volume.
- [Chapter 8](08-ot-ics-associate-architecture-sensors-and-asset-visibility.md) of this volume for the Purdue model, sensor architecture, and
  protocol dissection foundation this chapter builds on.
- [CERTIFICATION_BLUEPRINTS.md](../../../CERTIFICATION_BLUEPRINTS.md) —
  FSCA: OT/ICS and FSCE: OT/ICS blueprint domain mapping for this volume.
- Forescout Technologies certification and training catalog (official
  source for current FSCA: OT/ICS and FSCE: OT/ICS blueprint domains and
  exam registration).

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

**Objective.** Extend [Chapter 8](08-ot-ics-associate-architecture-sensors-and-asset-visibility.md)'s single-zone lab into a two-zone
topology with a curation pass and a behavioral-baseline alerting rule,
without enabling any control action.

**Prerequisites**

- The lab sensor/capture setup, PLC simulator, and Purdue-model diagram
  from [Chapter 8](08-ot-ics-associate-architecture-sensors-and-asset-visibility.md)'s lab.
- A second simulated zone (a second PLC simulator instance, or a second
  VLAN/segment on the lab switch representing a distinct cell/area zone)
  with its own SPAN session to a second sensor or capture point.
- A simple spreadsheet or text file to serve as the "asset register"
  enrichment source for the curation exercise.

**Procedure**

1. Extend the [Chapter 8](08-ot-ics-associate-architecture-sensors-and-asset-visibility.md) Purdue-model diagram to include the second
   simulated zone, labeled distinctly (for example, "Line 2 Cell
   Controllers" alongside the original "Line 1 Cell Controllers").
2. Configure the second zone's SPAN session and confirm passive
   visibility of its simulated PLC traffic, following the same procedure
   validated in [Chapter 8](08-ot-ics-associate-architecture-sensors-and-asset-visibility.md).
3. Create a simple asset register entry (make, approximate model,
   installation date) for each simulated PLC in your text file/
   spreadsheet, representing the engineering-source enrichment data
   curation draws on.
4. Perform a curation pass: compare each sensor-observed asset record
   against your asset register, and note any discrepancy (for example, an
   asset visible on the network with no corresponding register entry, or
   vice versa) as a curation finding.
5. Define a simple behavioral baseline for one zone (for example, "reads
   only, no write/program-download operations expected during normal
   lab operation") and then generate a deliberate write or
   program-download-style operation from the simulator to represent an
   anomalous event.
6. Confirm the anomalous operation is distinguishable from the baseline
   in your sensor or capture data (either through an actual alerting rule
   if your lab tool supports one, or by manually reviewing the capture
   against your documented baseline).
7. **Negative test.** Attempt to correlate the anomalous operation
   against a "change ticket" you deliberately do not create, and confirm
   your documented process would correctly escalate it as unapproved
   (unmatched to any change record) — then create a matching change
   record after the fact and confirm the same operation would now
   correlate as approved, demonstrating the escalation logic's
   dependency on timely change-management data.

**Expected Results**

- Both zones are independently visible with correctly attributed
  traffic, and the extended Purdue diagram accurately reflects the
  two-zone topology.
- The curation pass produces at least one documented discrepancy finding
  between sensor-observed assets and the asset register.
- The anomalous write/program-download operation is distinguishable from
  the defined baseline.
- The negative test demonstrates correct escalation behavior for an
  unmatched operation and correct correlation once a matching change
  record exists.

**Cleanup**

- Remove the second zone's SPAN session if the switch interfaces are
  needed elsewhere.
- Stop both PLC/protocol traffic simulators.
- Retain the curation findings, asset register, and updated Purdue
  diagram as artifacts for this chapter's design synthesis deliverable.

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
