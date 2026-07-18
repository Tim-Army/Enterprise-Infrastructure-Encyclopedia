# Chapter 03: Clarification, Compliance, and Control Policies

## Learning Objectives

- Describe the shared condition/action structure the policy engine uses
  across classification, clarification, compliance, and control policies.
- Explain the purpose of clarification policies and how they resolve
  low-confidence or unknown classification results.
- Differentiate a compliance policy (checks state, reports or remediates)
  from a control policy (changes network state directly) and identify
  when each is the correct tool.
- Design policy rule ordering, exceptions, and grace periods that avoid
  false-positive enforcement.
- Build a staged rollout plan that moves a policy from monitor mode to
  live enforcement with a documented rollback path.
- Select an appropriate control action (VLAN change, port restrict,
  endpoint isolation, notification, remediation script) for a given
  compliance failure scenario.

## Theory and Architecture

Chapter 2 introduced the host record and the property store as the shared
data model underlying every Forescout capability. This chapter covers the
three policy types built on top of that data model that move a deployment
from passive visibility to active governance: **clarification policies**,
**compliance policies**, and **control policies**. All three — along with
the classification policies introduced in Chapter 2 — share a single
structural pattern in the policy engine: a policy is an ordered set of
**rules**, each rule is a set of **conditions** evaluated against host
properties, and each rule fires one or more **actions** when its
conditions match. Understanding this shared structure is what makes the
platform's four policy types learnable as variations on one pattern rather
than four unrelated systems.

### The rule evaluation model

Within a single policy, rules are evaluated top-down against each host
in the policy's scope. A host is generally captured by the first rule
whose conditions it satisfies (higher rules take precedence over lower,
broader ones), and the matching rule's actions execute. Re-evaluation
happens continuously as properties change — a host that satisfies a
compliant rule today can fall out of compliance the moment a monitored
property changes (an antivirus service stops, a required patch-level
property ages out), and the engine will re-fire the matching rule for its
new state. This continuous evaluation is what allows compliance and
control policies to function as living governance rather than a one-time
audit.

### Clarification policies

Classification (Chapter 2) does not always produce a confident, actionable
result. A device might present a fingerprint the built-in classification
engine has never seen, or one where conflicting signals lower confidence
below a usable threshold. A **clarification policy** — often built from
the platform's "Clarify" policy template — targets exactly this
population: hosts whose classification is missing, generic, or below a
confidence threshold that later compliance and control policies depend on.

Clarification resolves ambiguity through one or more of:

- **Escalating discovery.** Triggering a more specific active scan or
  enabling a targeted plugin (for example, prompting an HPS inspection)
  against the ambiguous host to gather corroborating evidence.
- **Directed engagement.** For hosts capable of rendering a captive
  portal or receiving SecureConnector, presenting the end user with a
  short identification prompt (device type, business justification) that
  writes the answer back as a property.
- **Manual review queueing.** Adding the host to a group or dashboard
  view that routes it to a human reviewer (typically NOC/SOC staff) when
  automated escalation still leaves the classification unresolved.

The output of a clarification policy is not a network action — it is a
property update that raises classification confidence (or explicitly
tags the host as reviewed-and-still-unknown) so that downstream compliance
and control policies have a trustworthy input to evaluate. Treat
clarification as the bridge between "the platform sees a device" and "the
platform is confident enough about what the device is to govern it."

### Compliance policies

A **compliance policy** evaluates whether a host's current state matches a
defined desired state and records the result as a compliance status
property — it does not, by itself, change the host's network access.
Typical compliance checks include: security agent presence and running
state (antivirus, EDR, disk encryption), patch level or OS build currency,
prohibited software presence, and configuration baseline conformance
(for example, a required registry key or a disallowed local
administrator account). Compliance policies commonly support a **grace
period** — a window during which a newly non-compliant host is flagged
but not yet escalated to a control action, giving automated remediation
(for example, a UEM-triggered patch push) or the end user time to
self-correct before enforcement engages.

Compliance policies frequently pair with **remediation actions** — a
script push, a UEM/EDR API call, or an end-user notification — that
attempt to fix the underlying problem rather than only reporting it. A
well-designed compliance policy therefore has three tiers of response
mapped to elapsed non-compliance time: report only, then automated
remediation attempt, then (if still unresolved and control is licensed and
enabled) escalation to a control policy.

### Control policies

A **control policy** is the policy type that changes a host's actual
network state: assigning it to a quarantine or remediation VLAN,
restricting or blocking its switch port, applying an isolating ACL,
disconnecting a wireless session, or triggering a firewall/NAC vendor
integration to do the equivalent at a different enforcement point. Control
actions execute against the network infrastructure plugins (Switch,
Wireless) or eyeExtend integrations described in Chapter 2 — the appliance
does not need to sit inline to enforce, because it drives enforcement
through the management interface of infrastructure that is inline.

Common control actions, roughly ordered from least to most disruptive:

| Action | Effect |
| --- | --- |
| Notify | Send an email, syslog event, or dashboard alert; no network change. |
| Add to group / tag | Mark the host for tracking or for a downstream policy/report; no network change. |
| HTTP/webhook or script action | Invoke an external system (ticket creation, SOAR playbook) as a governance step. |
| VLAN reassignment | Move the host's switch port to a quarantine/remediation VLAN with restricted reachability. |
| Port restrict/ACL | Apply a port-level ACL limiting the host to specific destinations (commonly a remediation server and DNS). |
| Port block/disable | Administratively shut down the switch port or deny the wireless association entirely. |
| Endpoint isolation (SecureConnector) | Use the endpoint agent to enforce host-based network isolation independent of switch state. |

Because control actions are reversible only through a corresponding
"undo" action (re-enable the port, move back to the production VLAN),
every control policy should have a clearly defined re-admission
condition — the property state that, once restored, triggers the
platform to reverse the action automatically rather than requiring a
manual ticket for every remediated host.

## Design Considerations

- **Policy layering order.** Design classification and clarification to
  run and stabilize before compliance policies evaluate, and compliance
  to run before control policies act on compliance results. A control
  policy that reads a compliance status still settling from a
  classification change will act on stale or transitional data.
- **Grace periods calibrated to remediation SLA.** Set compliance grace
  periods to match how long automated remediation realistically takes
  (a patch push cycle, a UEM check-in interval) — a grace period shorter
  than the remediation SLA guarantees false-positive enforcement against
  hosts that are already correctly on their way to compliant.
- **Exceptions and exclusion groups.** Maintain an explicit, documented
  exclusion group (for example, isolated lab segments, medical devices
  under a change freeze, or infrastructure management interfaces) that
  every control policy checks against before acting, rather than relying
  on administrators to remember to exclude sensitive hosts rule by rule.
- **Monitor-mode staging.** Every new or materially changed control
  policy should run in monitor/simulate mode first — logging what it
  *would* do without doing it — over a representative observation
  window, so false positives surface against real traffic before any
  host is actually affected.
- **Escalation tiers and time-to-enforcement.** Decide, per compliance
  check, the full tier ladder (report → remediate → notify user → escalate
  to control) and the dwell time at each tier; do not jump directly from
  detection to network isolation for checks where a false positive causes
  significant business disruption.
- **Re-admission design.** For every control action, define the
  re-admission condition and confirm the policy engine's re-evaluation
  cadence will detect it promptly — a slow re-evaluation interval turns a
  fixed problem into an extended, unnecessary outage for the end user.
- **Auditability.** Compliance and control policy actions should log
  enough context (which rule matched, which property values triggered it,
  timestamp) to reconstruct why a specific host was quarantined during a
  post-incident review or an audit.

## Implementation and Automation

The following sequence builds a compliance policy with a paired control
policy, reflecting the staged approach recommended above. Exact menu
labels vary by release; consult the policy authoring guide for your
licensed 8.5.x build.

1. **Confirm classification/clarification stability** for the target host
   population (see Chapter 2) before authoring a compliance policy that
   depends on accurate `Function` or `Operating System` values.
2. **Author the compliance policy.** Define the desired-state condition
   (for example, a required endpoint security property showing
   `Running`) and a non-compliant condition (the property showing
   `Stopped`, `Not Installed`, or absent). A simplified pseudocode
   structure:

   ```text
   RULE "AV Not Running"
     IF  Function = "Windows Workstation"
     AND Antivirus Status != "Running"
     THEN set Compliance Status = "Non-Compliant: AV"
          start grace timer (4 hours)
          action: notify security-ops distribution list
   ```

3. **Add a remediation action** invoked at grace-period expiry if the
   property has not self-corrected — for example, an eyeExtend action
   that calls the EDR/UEM platform's API to restart the agent or push a
   remediation task.
4. **Author the paired control policy in monitor mode.** Reference the
   compliance policy's status property as the triggering condition, and
   set the policy to log/simulate rather than execute the control action:

   ```text
   RULE "Quarantine Non-Compliant Endpoint"
     IF  Compliance Status = "Non-Compliant: AV"
     AND Grace Period Expired = true
     AND Host NOT IN group "Exclusion - Managed Exceptions"
     THEN [MONITOR MODE] action: VLAN reassignment to "Remediation VLAN"
   ```

5. **Observe monitor-mode output** over an agreed window (commonly one to
   two weeks, depending on host population churn) and review every
   host the policy would have acted on for false positives.
6. **Tune conditions** based on the monitor-mode review — add
   corroborating conditions, adjust the grace period, or expand the
   exclusion group — before proceeding.
7. **Enable live enforcement** on a limited pilot scope (a single site,
   VLAN, or department) first, with an on-call escalation path
   documented for the rollout window.
8. **Define and test the re-admission rule** — confirm that once the
   triggering property returns to a compliant value, the platform
   automatically reverses the VLAN reassignment within an acceptable
   time window.
9. **Expand enforcement scope** incrementally once the pilot demonstrates
   an acceptable false-positive rate, following the same
   report-then-verify-then-expand pattern for each additional scope.

## Validation and Troubleshooting

- **A host is quarantined that should not have been.** Review the
  specific rule and property values that triggered the action from the
  policy's action log; most unexpected enforcement traces to a
  classification that was less stable than assumed, or an exclusion
  group that was not updated when the host's role changed.
- **A non-compliant host never gets remediated or escalated.** Confirm
  the grace-period timer actually started (a policy re-evaluation gap can
  delay timer start) and that the remediation action's target system
  (UEM/EDR API) is reachable and authenticating correctly.
- **A control action fires but does not take effect on the network.**
  Verify the underlying infrastructure plugin (Switch/Wireless) has a
  valid, sufficiently privileged write credential — read-only credentials
  scoped for visibility, as recommended in Chapter 2, will not support
  control actions and must be upgraded deliberately and only for the
  appliances performing enforcement.
- **A host stays quarantined after remediation.** Check the re-admission
  condition against the host's current properties; a common cause is a
  re-admission condition referencing a property that a different plugin
  updates on a slower polling interval than the compliance check that
  triggered quarantine.
- **Policy performance/evaluation lag** under high host churn. Review
  policy condition complexity (deeply nested or high-cardinality
  conditions evaluate more slowly) and confirm appliance sizing still
  matches current host count and property update volume, as covered in
  Chapter 1.

## Security and Best Practices

- Require a second reviewer or a change-management approval for any
  policy edit that could newly quarantine or block previously unaffected
  hosts, given the operational disruption a misconfigured control policy
  can cause at scale.
- Keep the exclusion group tightly scoped and reviewed on a fixed cadence
  — an exclusion group that only grows over time silently erodes
  enforcement coverage.
- Log every control action with enough detail to support incident
  reconstruction, and forward those logs to the organization's SIEM (see
  Chapter 5) rather than relying solely on the platform's local retention.
- Grant control-policy write credentials to network infrastructure on a
  least-privilege, appliance-scoped basis, separate from the read-only
  visibility credentials used elsewhere in the deployment.
- Build a documented, tested manual override procedure (a way to
  immediately re-admit a business-critical host, such as a life-safety or
  clinical device, that was incorrectly quarantined) that on-call staff
  can execute without deep platform expertise.
- Periodically review compliance policy definitions against current
  organizational security baselines; a compliance policy that has not
  been revisited since it was authored tends to drift out of alignment
  with the standards it was meant to enforce.

## References and Knowledge Checks

**References**

- Forescout Technologies policy authoring and Clarify/compliance/control
  policy template documentation for the 8.5.x release.
- [SOFTWARE_VERSIONS.md](../../../SOFTWARE_VERSIONS.md) — dated platform
  baseline for this volume.
- Chapter 2 of this volume for the classification and property model that
  clarification and compliance policies depend on.
- [CERTIFICATION_BLUEPRINTS.md](../../../CERTIFICATION_BLUEPRINTS.md) —
  FSCA/FSCP/FSCE blueprint domain mapping for this volume.

**Knowledge Checks**

1. What is the functional difference between a compliance policy and a
   control policy, and why does control policy logic typically read a
   compliance policy's output rather than evaluating raw properties
   directly?
2. Describe two mechanisms a clarification policy can use to resolve a
   low-confidence classification, and explain what property change
   signals success.
3. Why should a new control policy run in monitor/simulate mode before
   live enforcement, and what specifically should be reviewed during that
   period?
4. What problem does a grace period solve, and what happens when it is
   set shorter than the realistic remediation time?
5. Why must a re-admission condition be explicitly defined and tested for
   every control action, rather than assumed?

## Hands-On Lab

**Objective.** Build a compliance policy with a grace period and a paired
control policy staged through monitor mode, then validate both the
enforcement and re-admission paths.

**Prerequisites**

- The lab appliance and Console from Chapters 1–2, with at least one
  classified test endpoint.
- A custom property (reuse `Lab Asset Owner` from Chapter 2, or create a
  new boolean property named `Lab Agent Running`) that you can toggle
  manually to simulate a compliance state change.
- Console access with permission to create and enable policies.
- A lab switch port or VLAN designated as a harmless "remediation" target
  (no production dependency) for the control action.

**Procedure**

1. Set the `Lab Agent Running` custom property to `true` on your test
   endpoint to represent an initial compliant state.
2. Author a compliance policy rule: `IF Lab Agent Running = false THEN
   set Compliance Status = "Non-Compliant: Lab" with a 10-minute grace
   period`. Use a short grace period so the lab is practical to run in one
   session.
3. Author a control policy rule in **monitor mode**: `IF Compliance
   Status = "Non-Compliant: Lab" AND grace period expired THEN VLAN
   reassignment to the lab remediation VLAN`.
4. Toggle `Lab Agent Running` to `false` on the test endpoint and confirm
   the compliance policy sets `Compliance Status` to `Non-Compliant: Lab`.
5. Wait for the grace period to expire and confirm the control policy's
   monitor-mode log shows the action it *would* have taken, without the
   endpoint's actual VLAN changing.
6. Switch the control policy from monitor mode to live enforcement, reset
   `Lab Agent Running` to `false` again (or force re-evaluation), and
   confirm the test endpoint is actually reassigned to the lab
   remediation VLAN this time.
7. Set `Lab Agent Running` back to `true` and confirm the re-admission
   path returns the endpoint to its original VLAN within one policy
   re-evaluation cycle.
8. **Negative test.** Add the test endpoint to an exclusion group, force
   `Lab Agent Running` to `false` again, and confirm the control policy
   does **not** act on the excluded host despite matching the compliance
   condition — this validates that your exclusion-group logic actually
   takes precedence, which is the same safety mechanism production
   deployments rely on to protect sensitive hosts.

**Expected Results**

- The compliance policy correctly transitions `Compliance Status` after
  the grace period, and the control policy's monitor-mode log accurately
  previews the action before live enforcement is enabled.
- Live enforcement correctly reassigns the VLAN, and the re-admission
  condition correctly reverses it once the underlying property is
  restored.
- The negative test confirms the exclusion group prevents enforcement
  against a protected host.

**Cleanup**

- Disable or delete the lab compliance and control policy rules if they
  should not persist.
- Remove the test endpoint from the exclusion group and confirm its VLAN
  assignment is back to its original state.
- Leave `Lab Agent Running` in place if later chapter labs may reuse it;
  otherwise remove it.

## Summary and Completion Checklist

This chapter extended the policy engine model from Chapter 2 into the
three policy types that turn visibility into governance: clarification
policies that resolve classification ambiguity, compliance policies that
evaluate and report desired-state conformance with grace-period-driven
remediation, and control policies that change actual network state. It
covered the shared rule/condition/action structure, the ordered relationship
between policy types (classification/clarification feeding compliance,
compliance feeding control), and the staged monitor-mode-to-enforcement
rollout pattern that keeps control policies from causing unplanned
disruption.

**Completion checklist**

- [ ] Can explain the shared condition/action structure across
      classification, clarification, compliance, and control policies.
- [ ] Can describe what a clarification policy resolves and what
      downstream policies depend on that resolution.
- [ ] Can distinguish a compliance policy's reporting/remediation role
      from a control policy's network-state-changing role.
- [ ] Completed the hands-on lab, including monitor-mode validation, live
      enforcement, re-admission, and the exclusion-group negative test.
- [ ] Understands why grace periods, exclusion groups, and re-admission
      conditions are mandatory design elements, not optional refinements.
