# Chapter 06: Advanced Troubleshooting, Performance, and Resilience

![Lab flow for this chapter: baseline resource metrics are recorded, increased active-scan intensity produces an observable effect that reverts once undone, and a layered diagnostic write-up for a slow Console works down from network delivery through appliance health, plugin, and policy layers. A configuration backup is taken, restored, and validated by confirming at least one policy and one custom property survived correctly. As a negative test, a plugin's credential is changed only in its own configuration, not on the target device; the plugin layer surfaces a clear authentication/connectivity failure distinct from a network-delivery failure, and reverting the credential restores clean operation.](../../../diagrams/volume-15-forescout-platform-certifications/chapter-06-layered-diagnosis-plugin-failure-flow.svg)

*Figure 6-1. Flow used throughout this chapter's Hands-On Lab: baseline resource metrics, a layered diagnostic model, and a validated backup/restore, tested against a plugin credential failure.*

## Learning Objectives

- Apply a structured diagnostic method to platform issues that spans
  appliance health, plugin state, policy evaluation, and network delivery.
- Use appliance-level diagnostics (logs, resource metrics, and, where
  appropriate, packet capture) to isolate visibility and enforcement
  failures.
- Tune appliance and plugin performance for high host-count or
  high-churn environments.
- Design high-availability and disaster-recovery postures for the
  Enterprise Manager and appliance tier appropriate to a control-capable
  deployment.
- Execute and validate a backup/restore and appliance-replacement
  procedure without data loss or extended enforcement gaps.
- Distinguish transient performance degradation from a capacity ceiling
  that requires a sizing change.

## Theory and Architecture

Chapters 1–5 covered building and operating a Forescout deployment under
normal conditions. Production deployments also need a structured approach
to what happens when something is not normal: a visibility gap, an
enforcement action that silently stops firing, a Console that is slow
under load, or an appliance failure during a control-capable enforcement
window. This chapter treats troubleshooting as a layered diagnostic
discipline rather than a list of unrelated symptoms, and covers the
performance-tuning and resilience design that reduces how often that
discipline needs to be invoked.

### A layered diagnostic model

Because the platform's behavior at any given host is the product of
several independent layers — network delivery, appliance health, plugin
data collection, property state, and policy evaluation — an effective
diagnostic method works top-down through those layers rather than
guessing at the specific policy or plugin first:

1. **Network delivery layer.** Is the relevant traffic (SPAN/mirror
   feed, active scan path, plugin management-interface reachability)
   actually arriving at the appliance? [Chapter 1](01-platform-architecture-installation-and-deployment-planning.md) covered this layer for
   initial deployment; it remains the first check for any later
   "hosts stopped updating" symptom too.
2. **Appliance health layer.** Is the appliance itself healthy — CPU,
   memory, disk, process/service state — or is a resource ceiling
   silently degrading its ability to process what it is receiving?
3. **Plugin layer.** Is the specific plugin expected to supply the
   affected data actually connected, authenticated, and polling on
   schedule? ([Chapter 2](02-console-plugins-properties-and-asset-classification.md)'s plugin status/diagnostic pane is the primary
   tool here.)
4. **Property/policy layer.** Given correct plugin data, is the
   classification, compliance, or control policy evaluating the property
   correctly and in the expected order? ([Chapter 3](03-clarification-compliance-and-control-policies.md)'s action history is
   the primary tool here.)
5. **Downstream/integration layer.** For control actions or eyeExtend
   integrations, did the downstream system (switch, firewall, external
   platform) actually receive and apply the requested change? ([Chapter 5](05-advanced-policy-integrations-and-business-outcomes.md)'s
   integration status views are the primary tool here.)

Working through these layers in order avoids the common troubleshooting
error of tuning a policy rule when the actual fault is an appliance
resource ceiling two layers below it.

### Appliance-level diagnostics

Beyond the health dashboards covered in [Chapter 4](04-host-management-administration-inventory-and-reporting.md), deeper diagnosis
sometimes requires appliance-native tools:

- **System and plugin logs.** Each appliance retains logs for its own
  system processes and for individual plugins; log verbosity is
  typically adjustable per plugin for a bounded troubleshooting window
  without leaving elevated logging enabled permanently (which itself
  becomes a performance and disk-consumption concern).
- **Resource metrics history.** CPU, memory, disk I/O, and interface
  throughput trends over time (not just current-instant values) are what
  distinguish a transient spike from a sustained capacity ceiling.
- **Targeted packet capture.** For SPAN/mirror delivery problems that
  survive the basic checks in [Chapter 1](01-platform-architecture-installation-and-deployment-planning.md) (link up, correct VLAN sourced),
  a time-boxed packet capture on the monitor interface confirms whether
  expected traffic is actually arriving, and at what volume relative to
  the interface's capacity.
- **Policy evaluation tracing.** Where available, a policy's evaluation
  trace for a specific host shows which rule matched (or why none did)
  at the moment of evaluation — more precise than inferring rule logic
  from the resulting property state alone.

### Performance tuning drivers

As established in [Chapter 1](01-platform-architecture-installation-and-deployment-planning.md), appliance capacity is driven primarily by
concurrent host count and property update churn rather than raw link
bandwidth. Performance tuning therefore concentrates on:

- **Scan intensity and scheduling.** Reducing active scan frequency or
  concurrency on high-host-count segments, and scheduling
  bandwidth-sensitive scans outside business-critical windows.
- **Plugin polling interval.** Lengthening polling intervals for plugins
  whose data does not need near-real-time freshness (a weekly-refreshed
  CMDB integration, for example) frees appliance and network capacity for
  plugins that do.
- **Policy condition efficiency.** Simplifying deeply nested or
  high-cardinality policy conditions, and ensuring frequently evaluated
  conditions reference indexed/built-in properties rather than expensive
  custom-property text matching wherever possible.
- **Appliance role specialization.** In larger deployments, dedicating
  specific appliances to specific plugin workloads (for example, isolating
  HPS/endpoint-inspection load onto appliances not also carrying heavy
  SPAN traffic processing) rather than running every plugin on every
  appliance.
- **Enterprise Manager sizing relative to total managed host count**,
  re-validated periodically as the deployment grows rather than assumed
  fixed from initial sizing.

### High availability and resilience

Because eyeControl-enabled deployments can be relied on for real-time
enforcement decisions, resilience design has to consider both
data-plane visibility loss and enforcement-capability loss:

- **Enterprise Manager high availability.** Deployments with a
  control-capable, business-critical posture typically pair the EM with
  a standby instance or a documented, tested rebuild procedure, since EM
  loss affects centralized policy distribution and consolidated
  reporting even if individual appliances continue local enforcement.
- **Appliance redundancy for critical enforcement points.** For any
  segment where a control action is compliance- or security-critical
  ([Chapter 1](01-platform-architecture-installation-and-deployment-planning.md)), determine whether a single appliance failure removes that
  enforcement capability entirely, and pair critical appliances or define
  a compensating manual procedure if hardware redundancy is not
  practical.
- **Graceful degradation on central-management loss.** Because policy
  evaluation happens locally on each appliance ([Chapter 1](01-platform-architecture-installation-and-deployment-planning.md)), a temporary
  EM outage should not halt in-progress enforcement on healthy
  appliances — confirm this behavior is understood and tested rather than
  assumed.
- **Disaster recovery.** A documented, periodically tested procedure for
  rebuilding an appliance or the EM from backup ([Chapter 4](04-host-management-administration-inventory-and-reporting.md)) onto
  replacement hardware or a new virtual instance, including how long a
  full rebuild is expected to take and what visibility/enforcement gap
  exists during that window.

## Design Considerations

- **Diagnostic runbook ownership.** Document the layered diagnostic
  model above as an actual on-call runbook, not only as training
  material, so that a first responder under incident pressure has a
  concrete starting sequence rather than needing platform expertise to
  improvise one.
- **Elevated logging discipline.** Treat verbose/debug logging as a
  temporary, time-boxed diagnostic state that is explicitly reverted,
  since permanently elevated logging degrades performance and can fill
  disk on constrained appliance storage.
- **Capacity headroom vs. cost.** Decide, deliberately, how much capacity
  headroom above current peak load the organization is willing to pay
  for — under-provisioning risks the degraded-performance failure modes
  covered above; over-provisioning is a real, avoidable cost.
- **RTO/RPO for the platform itself.** Set an explicit recovery time
  objective and recovery point objective for the EM and for
  critical-enforcement appliances, driven by how much visibility or
  enforcement gap the business can actually tolerate, and size the HA/DR
  investment to match rather than defaulting to "as resilient as
  possible."
- **Blast radius of a bad performance-tuning change.** Changes like
  lengthening a plugin's polling interval trade data freshness for
  capacity; make this trade-off visible to the policies and reports that
  depend on that data's freshness before applying it broadly.
- **Test environment parity.** Where practical, validate significant
  performance-tuning or HA/DR procedure changes in a non-production
  environment sized similarly to production, since appliance behavior
  under load does not always reveal itself at lab scale.

## Implementation and Automation

1. **Establish baseline resource metrics** for every appliance and the
   EM during known-healthy operation, so future degradation has a
   reference point rather than only an absolute threshold.
2. **Configure alerting thresholds** for CPU, memory, disk, and
   monitor-interface state (extending [Chapter 4](04-host-management-administration-inventory-and-reporting.md)'s health monitoring)
   tuned against that baseline rather than generic defaults.
3. **Build and rehearse the layered diagnostic runbook** covering network
   delivery, appliance health, plugin state, property/policy state, and
   downstream/integration state, using a real (or simulated) past
   incident as the walkthrough scenario.
4. **Tune scan and plugin polling schedules** for the highest-host-count
   segments first, since they yield the largest capacity return per
   tuning change; re-measure appliance resource metrics after each
   change to confirm the intended effect.
5. **Review and simplify policy conditions** flagged as expensive during
   performance review (Validation and Troubleshooting below), prioritizing
   policies that evaluate against the largest host populations.
6. **Design and document the EM and critical-appliance HA/DR posture**,
   including the specific RTO/RPO target for each tier and the concrete
   steps to execute a failover or rebuild.
7. **Schedule a recurring DR test** (for example, semi-annual) that
   actually restores a backup onto a non-production appliance or EM
   instance and validates functional correctness, not only that the
   restore operation completes without error.
8. **Document a graceful-degradation validation test** — a controlled,
   scheduled EM outage simulation confirming appliance-local enforcement
   continues correctly during the outage window.

## Validation and Troubleshooting

- **Console or EM is slow under normal load.** Work the layered model
  top-down: confirm EM resource metrics against baseline before assuming
  a database or query-performance problem; a resource ceiling reached
  from unplanned host-count growth ([Chapter 1](01-platform-architecture-installation-and-deployment-planning.md)) is a more common root
  cause than a software defect.
- **Hosts intermittently drop out of the inventory and reappear.** Check
  monitor-interface link stability and SPAN/tap delivery consistency
  first (network delivery layer) before investigating plugin or policy
  logic — intermittent physical or switch-side SPAN issues produce
  exactly this symptom.
- **A control action worked yesterday and silently stopped today.**
  Check the downstream/integration layer specifically — an expired or
  rotated credential on the target switch, firewall, or eyeExtend
  integration is a common cause of an enforcement action that appears to
  fire (per the action history) but does not actually apply.
- **Performance degrades specifically during active-scan windows.**
  Correlate the timing precisely; if degradation tracks scan schedule,
  reduce scan concurrency/intensity on the affected segment rather than
  increasing appliance sizing first, since the fix is often
  scheduling-based, not capacity-based.
- **A DR restore succeeds technically but policies behave differently
  afterward.** Confirm the restored configuration version matches the
  live platform software version; restoring a configuration backup onto a
  mismatched software version is a common source of subtle
  policy-behavior drift after a DR event.
- **Appliance resource metrics look fine but a specific plugin is slow.**
  Isolate the plugin's own polling/response-time metric rather than
  relying only on whole-appliance CPU/memory, since a single
  slow-responding external system (a switch under its own load, for
  example) can bottleneck one plugin without materially affecting overall
  appliance resource consumption.

## Security and Best Practices

- Restrict elevated/debug logging access and enforce its time-boxed
  reversion through the same change-management discipline as other
  configuration changes, since verbose logs can capture sensitive data
  (credentials in transit, endpoint detail) that should not be retained
  longer than necessary.
- Protect DR backup and restore infrastructure with the same access
  controls and encryption-at-rest expectations as production
  ([Chapter 4](04-host-management-administration-inventory-and-reporting.md)), since a DR environment is a full copy of the platform's
  sensitive configuration and, potentially, inventory data.
- Ensure HA/DR failover procedures preserve, rather than silently
  bypass, RBAC and audit-logging configuration — a rebuilt appliance or
  EM that reverts to default credentials or loses its access-control
  configuration during recovery is a realistic post-incident exposure.
- Validate that graceful-degradation behavior (local enforcement
  continuing during EM outage) does not also mean an attacker who
  disrupts the EM can prevent updated compliance/control policy from
  reaching appliances indefinitely without alerting; alert distinctly on
  EM-to-appliance sync failures, not only on EM availability.
- Include platform resilience testing (DR restore, degradation
  simulation) in the same operational exercise cadence as other
  business-critical systems, so platform recovery procedures are
  proven, not assumed, before an actual incident.

## References and Knowledge Checks

**References**

- [Forescout Technologies appliance diagnostics, performance tuning, and
  high-availability/disaster-recovery administration guides for the
  8.5.x release.](https://docs.forescout.com/)
- [SOFTWARE_VERSIONS.md](../../../SOFTWARE_VERSIONS.md) — dated platform
  baseline for this volume.
- Chapters 1 and 4 of this volume for the sizing and platform
  administration foundations this chapter extends.
- [CERTIFICATION_BLUEPRINTS.md](../../../CERTIFICATION_BLUEPRINTS.md) —
  FSCA/FSCP/FSCE blueprint domain mapping for this volume.

**Knowledge Checks**

1. Describe the five layers of the diagnostic model in this chapter and
   why working through them top-down avoids a common troubleshooting
   error.
2. Why does appliance capacity tuning concentrate on host count and
   churn rather than raw link bandwidth, and name two concrete tuning
   levers that follow from that.
3. Why should EM-to-appliance sync failures be alerted on distinctly from
   EM availability, given that appliances continue local enforcement
   during a central-management outage?
4. What is the difference between a DR restore that "completes without
   error" and one that is functionally validated, and why does that
   distinction matter?
5. Give one example of a performance-tuning change that trades data
   freshness for capacity, and describe how to make that trade-off
   visible to stakeholders before applying it.

## Hands-On Lab

**Objective.** Establish a resource-metric baseline, simulate a
performance-degradation scenario and diagnose it using the layered model,
and perform a validated backup/restore drill.

**Prerequisites**

- The lab appliance and Console from Chapters 1–5, with policies from
  earlier labs in place.
- Access to appliance resource-metric views (or equivalent host-level
  metrics if using a virtual lab appliance monitored externally).
- Permission to trigger and restore a configuration backup, and, ideally,
  a second non-production appliance or instance to restore onto (a
  duplicate lab deployment is acceptable; if unavailable, document the
  restore procedure as a dry run against the same instance's backup
  history instead).

**Procedure**

1. Record baseline CPU, memory, and disk metrics for the lab appliance
   during idle/normal operation.
2. Temporarily increase active-scan intensity/concurrency on the lab
   subnet (or, if lab scale is too small to observe a real effect,
   document the expected relationship and the specific setting that would
   be adjusted in a larger environment) and observe the resulting metric
   change relative to baseline.
3. Using the layered diagnostic model, write a short diagnostic log
   entry as if investigating "Console feels slow" starting from network
   delivery and working down — noting at each layer what you checked and
   what you would conclude if that layer were the fault.
4. Revert the scan intensity change and confirm metrics return toward
   baseline.
5. Trigger a configuration backup (reuse the [Chapter 4](04-host-management-administration-inventory-and-reporting.md) lab's backup step
   if still valid, or take a fresh one) and record its completion
   timestamp and size.
6. Restore the backup — onto a second instance if available, or as a
   documented dry-run procedure against the same instance otherwise — and
   validate functional correctness afterward by confirming at least one
   policy and one custom property from earlier labs are present and
   correctly configured post-restore.
7. **Negative test.** Deliberately point a plugin at an invalid or
   revoked credential (for example, temporarily changing the Switch
   plugin's SNMP community string in the plugin configuration only,
   without changing it on the switch) and confirm the plugin layer
   surfaces a clear authentication/connectivity failure distinct from a
   network-delivery failure — then revert the credential and confirm
   recovery.

**Expected Results**

- The scan-intensity change produces an observable (or documented,
  if lab-scale limited) resource-metric effect, and reverting it returns
  metrics toward baseline.
- The layered diagnostic write-up correctly separates network delivery,
  appliance health, plugin, property/policy, and downstream/integration
  checks.
- The backup restores successfully and is functionally validated against
  at least one known policy and property, not just a completion status.
- The negative test produces a clearly attributable plugin-layer failure
  and clean recovery after the credential is reverted.

**Cleanup**

- Confirm scan intensity settings are restored to their pre-lab values.
- Confirm the Switch plugin credential is restored to its correct,
  working value.
- Remove or archive the restored duplicate instance if one was created
  only for this lab's restore drill.

## Lab Verification

Complete this sign-off once the lab has been run end to end, including the
negative test. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

This chapter built a structured, layered approach to diagnosing platform
issues — network delivery, appliance health, plugin state,
property/policy state, and downstream/integration state — and connected
it to the performance-tuning levers (scan intensity, polling interval,
policy condition efficiency, appliance role specialization) that reduce
how often deep troubleshooting is needed. It covered high-availability and
disaster-recovery design for the Enterprise Manager and critical-enforcement
appliances, including graceful degradation during central-management
outages, and emphasized functional validation of DR restores over mere
completion status.

**Completion checklist**

- [ ] Can describe and apply the five-layer diagnostic model in order.
- [ ] Can name at least three performance-tuning levers and the
      trade-off each involves.
- [ ] Can distinguish EM availability from EM-to-appliance sync health
      and explain why both need distinct alerting.
- [ ] Completed the hands-on lab, including the layered diagnostic
      write-up, the validated backup/restore drill, and the plugin
      credential negative test.
- [ ] Understands why DR restores must be functionally validated, not
      only confirmed to complete.
