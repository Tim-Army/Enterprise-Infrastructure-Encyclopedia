# Chapter 07: Service Management, Incident, Problem, and Change Operations

## Learning Objectives

- Distinguish incident management, problem management, and change
  management as related but structurally different ITIL 4 practices, and
  explain why conflating them causes process failures.
- Run a major incident using a defined command structure: incident
  commander, communications lead, and operations lead roles.
- Write a blameless postmortem that identifies contributing factors and
  produces tracked, owned action items rather than a narrative alone.
- Apply root cause analysis techniques (the Five Whys, a contributing-
  factors model) to convert a resolved incident into a permanent fix via
  problem management.
- Classify a change by risk category (standard, normal, emergency) and
  route it through the correct approval path.
- Diagnose common service-management process failures: incidents closed
  without a postmortem, problems left permanently open, and changes that
  bypass the change record entirely.

## Theory and Architecture

### Three related, distinct practices

ITIL 4 (introduced at the framework level in [Volume I, Chapter 08](../../volume-01-enterprise-engineering-foundations/chapters/08-infrastructure-lifecycle-management.md)) treats
incident, problem, and change as separate practices because they answer
different questions and operate on different timescales, and collapsing
them into one undifferentiated "ops process" is a common source of
dysfunction:

- **Incident management** answers "how do we restore service right now."
  It is fast, tactical, and success is measured by time to restoration,
  not by understanding root cause — a workaround that restores service
  in five minutes is a successful incident response even if the
  underlying defect is still present afterward.
- **Problem management** answers "why did this happen, and how do we
  make sure it does not happen again." It is slower and deliberate,
  operating after the incident is resolved, and its output is a
  permanent fix or a documented, accepted risk — not a restored service,
  since service is already restored by the time problem management
  engages.
- **Change management** answers "how do we make a deliberate
  modification to production safely." It is preventive rather than
  reactive: its job is to reduce the rate at which changes themselves
  become the next incident's root cause, which — across most
  well-instrumented enterprises — they disproportionately are.

The three connect in a loop: an incident, once resolved, feeds problem
management for root cause work; problem management's fix is itself a
change that must pass through change management; and a poorly managed
change is a leading cause of the next incident. A mature observability
and operations practice treats this as one connected lifecycle, not
three unrelated tickets in three different systems.

### Incident management and the major incident process

Most incidents are handled by the on-call responder alone, following the
runbook pattern from [Chapter 06](06-actionable-alerting-on-call-and-operations-centers.md), and close without escalation. A
**major incident** process activates when impact or ambiguity exceeds
what a single on-call responder should be expected to resolve alone —
typically triggered by Tier 0 service impact, multi-service
simultaneous degradation, or an incident that has run past a defined
time threshold (commonly 30 minutes) without a clear path to resolution.
The major incident process assigns three distinct roles, deliberately
separated so no one person is both fighting the fire and communicating
about it:

- **Incident Commander (IC)** — owns the incident end to end: directs
  the technical response, makes the call on drastic mitigations (a
  rollback, a failover, a feature-flag kill switch), and decides when
  the incident is resolved. The IC does not have to be the most senior
  engineer present or the person who understands the failing component
  best — the IC's job is coordination and decision authority, not deep
  technical execution, and a good IC actively delegates technical
  investigation rather than performing it personally.
- **Operations Lead** — drives the technical investigation and
  mitigation work directly, coordinating any additional engineers pulled
  in, and reports status to the IC rather than making unilateral
  decisions about incident-wide actions (a full rollback, a customer
  communication) without IC sign-off.
- **Communications Lead** — owns internal and external status
  communication (a status page update, an internal stakeholder channel,
  executive updates) on a fixed cadence, freeing the IC and operations
  lead from the cognitive load of drafting updates mid-investigation and
  ensuring communication does not silently stop just because the
  technical work is hard.

```text
Alert fires (Chapter 06) --> On-call acknowledges, begins triage
        |
        v
   Resolved solo? -----------------------------> Yes --> close, log for review
        | No (Tier 0 impact / ambiguous / >30min)
        v
   Major incident declared
        |
        +--> Incident Commander assigned
        +--> Operations Lead assigned
        +--> Communications Lead assigned
        |
        v
   Mitigation applied, impact confirmed resolved
        |
        v
   Incident formally closed --> Postmortem scheduled (Problem Mgmt begins)
```

Declaring a major incident should be a low-friction, blameless action —
any responder should be able to declare one without needing permission,
because the cost of declaring unnecessarily (a short call that
determines the situation was actually manageable solo) is far lower than
the cost of a real major incident running without coordinated command
for longer than necessary while someone hesitates to escalate.

### Incident severity classification

A consistent severity scale, distinct from the service tiering in
[Chapter 01](01-observability-operating-model-and-service-ownership.md) (tiering describes the service; severity describes the
current incident), drives response urgency and communication cadence:

| Severity | Definition | Major incident process | Communication cadence |
| --- | --- | --- | --- |
| SEV1 | Full outage of a Tier 0 service, or data loss/corruption risk | Always activated | Every 15-30 minutes |
| SEV2 | Significant degradation of a Tier 0/1 service | Activated if unresolved past threshold | Every 30-60 minutes |
| SEV3 | Limited impact, workaround available | Solo on-call handling | On resolution |
| SEV4 | Cosmetic or negligible impact | Ticket-based, no paging | None required |

### Problem management and root cause analysis

Problem management begins once the incident is resolved and asks a
structurally different question than incident response did. The **Five
Whys** technique is a simple, effective starting point — repeatedly
asking "why" against each answer until reaching a root cause rather than
stopping at the first proximate cause:

```text
1. Why did checkout-api return errors? -> The database connection pool was exhausted.
2. Why was the pool exhausted? -> A slow query held connections far longer than normal.
3. Why was the query slow? -> A missing index after a recent schema migration.
4. Why was the index missing? -> The migration's index-creation step was
   skipped in a fast-follow deploy under time pressure.
5. Why was that allowed? -> The migration checklist has no automated
   gate verifying all planned indexes exist post-migration.
```

The Five Whys' value is real but limited to single-cause narratives; most
real incidents have multiple **contributing factors** that combined to
produce impact, and a single linear chain understates that. A
contributing-factors model captures this more accurately: the missing
index was necessary but not sufficient — the incident also required the
connection pool to have no circuit breaker, the alert that would have
caught pool exhaustion earlier to have too loose a threshold, and the
on-call engineer's runbook to lack a diagnostic step for this specific
symptom. Effective problem management produces multiple independent
action items addressing multiple contributing factors, not one single
fix that addresses only the most proximate cause and leaves the system
one different missing safeguard away from a similar incident.

A **Known Error Database (KEDB)**, an ITIL 4 concept, records a
diagnosed root cause and its accepted workaround for a problem that is
not yet permanently fixed, so a future incident matching the same
symptom is recognized immediately by on-call rather than
re-investigated from scratch — converting expensive, repeated
diagnostic work into a one-time investment that pays off on every
recurrence until the underlying problem is actually closed.

### Blameless postmortems

A postmortem (also called a retrospective or after-action review) is the
primary artifact problem management produces. "Blameless" is a specific,
deliberate methodological stance, not a euphemism for avoiding
accountability: it treats human error as a symptom of systemic
conditions (unclear signals, missing safeguards, competing pressures)
rather than as a root cause in itself, on the premise that "the engineer
should have been more careful" is never an actionable finding and
punishing individual error reliably teaches people to hide near-misses
rather than surface them — directly undermining the organization's
ability to learn from what actually happened. A blameless postmortem
document includes:

- A precise timeline (ideally reconstructed from the actual telemetry —
  alert-fire timestamps, deploy timestamps, trace and log evidence —
  rather than from memory alone, which is unreliable under stress).
- Impact, quantified (duration, affected users or requests, error-budget
  consumed per [Chapter 03](03-metrics-service-level-objectives-and-error-budgets.md)).
- Contributing factors, not a single "root cause" line.
- Action items, each with a named owner and a tracked ticket, distinct
  from general narrative — an action item that is not tracked to
  completion in the same system as other engineering work reliably does
  not get done.
- What went well, explicitly — reinforcing effective response behavior
  is as valuable as identifying gaps, and omitting it makes postmortems
  feel purely punitive even when blameless in intent.

## Design Considerations

- **Postmortem trigger threshold.** Require a postmortem for every SEV1
  and SEV2 incident unconditionally, and make it available on request
  for any incident a responder felt was a near-miss — a rigid
  threshold-only trigger misses valuable near-miss learning that never
  became visible impact.
- **Action item follow-through governance.** An organization that
  produces excellent postmortems but never completes the resulting
  action items has a governance gap, not a documentation gap. Track
  postmortem action item completion rate as its own metric, reviewed at
  the same cadence as error budgets ([Chapter 03](03-metrics-service-level-objectives-and-error-budgets.md)), and treat a
  chronically incomplete action item backlog as its own signal for
  problem management to escalate.
- **Change risk classification granularity.** Too few risk categories
  (everything is "normal," requiring the same approval regardless of
  actual risk) creates unnecessary friction for genuinely low-risk
  changes and, paradoxically, encourages teams to route around the
  process entirely for routine work. Too many categories creates
  classification overhead that slows the change record itself. Three
  categories (standard, normal, emergency, per [Volume I Chapter 08](../../volume-01-enterprise-engineering-foundations/chapters/08-infrastructure-lifecycle-management.md)) is
  the common, workable default; refine sub-categories only where a
  specific class of change genuinely needs different handling (a
  database schema change versus a configuration flag flip).
- **Emergency change discipline.** An emergency change bypasses the
  normal pre-approval path specifically to remediate an active incident
  or imminent risk, and that speed is legitimate — but every emergency
  change must still be recorded and reviewed retrospectively, or the
  emergency path becomes a routinely used shortcut around governance
  rather than the genuine exception it is meant to be.
- **Incident-versus-problem system separation.** Deciding whether
  incidents and problems live in the same ticketing system with a type
  field, or in structurally separate systems, is a real trade-off:
  co-location makes the incident-to-problem link automatic and visible;
  separation can better protect problem management's slower, more
  deliberate cadence from getting mixed into the urgency of active
  incident queues. Either can work; what matters is that every SEV1/SEV2
  incident produces a traceable link to its problem record, not that a
  specific tool topology is used.
- **Who has authority to declare a major incident and end one.**
  Deliberately keep the bar to *declare* low (any responder, see Theory
  above) while keeping the bar to *stand down* slightly higher (IC
  confirmation that impact is genuinely resolved, not just that alerts
  stopped firing, since an alert clearing does not always mean the
  underlying condition is fully resolved).

## Implementation and Automation

Encode change risk classification as a structured record, integrated with
the same service catalog metadata from [Chapter 01](01-observability-operating-model-and-service-ownership.md) so risk category can be
partly auto-suggested from the target service's tier:

```yaml
# change-records/2026-07-18-checkout-api-index-migration.yaml
change_id: CHG-2026-0714
service: checkout-api
requested_by: alice@example.com
risk_category: normal   # standard | normal | emergency
summary: Add missing index on orders.customer_id to resolve CHG-linked problem PRB-0091
linked_problem: PRB-0091
linked_incident: INC-2026-0442
rollback_plan: >
  Drop the newly created index; no application code depends on its
  presence, so rollback is a single reversible DDL statement.
change_window:
  start: 2026-07-20T02:00:00-04:00
  end: 2026-07-20T02:30:00-04:00
approvals:
  - approver: group:payments-platform-team-lead
    status: approved
    timestamp: 2026-07-18T16:02:00-04:00
  - approver: group:database-reliability-team
    status: approved
    timestamp: 2026-07-18T17:40:00-04:00
```

Gate a deployment pipeline on a valid, approved change record for any
change classified above `standard`, closing the gap between "a change
record exists" and "the change record was actually required before
deploy proceeded":

```bash
#!/usr/bin/env bash
# require-change-approval.sh — CI gate before a normal/emergency deploy
set -euo pipefail

CHANGE_FILE="$1"
risk=$(yq '.risk_category' "$CHANGE_FILE")

if [[ "$risk" == "standard" ]]; then
  echo "Standard change; pre-approved runbook, proceeding."
  exit 0
fi

approved_count=$(yq '[.approvals[] | select(.status == "approved")] | length' "$CHANGE_FILE")
required_count=2

if [[ "$approved_count" -lt "$required_count" ]]; then
  echo "BLOCKED: $CHANGE_FILE has $approved_count/$required_count required approvals"
  exit 1
fi

echo "Change $(yq '.change_id' "$CHANGE_FILE") approved; proceeding."
```

A blameless postmortem template, structured to force the contributing-
factors and tracked-action-item disciplines from the Theory section
rather than allowing a narrative-only document:

```markdown
# Postmortem: INC-2026-0442 — checkout-api elevated error rate

**Severity:** SEV2  **Duration:** 47 minutes
**Error budget consumed:** 14% of 30-day availability budget

## Timeline (UTC, reconstructed from alert/deploy/trace evidence)
- 14:32:07 — CheckoutAPIAvailabilitySLOPageBurn fires (page threshold).
- 14:33:40 — On-call acknowledges, begins triage.
- 14:41:00 — Major incident declared (SEV2, impact ambiguous past 8 min).
- 14:52:00 — Root cause identified: connection pool exhaustion from a
  slow query.
- 15:09:00 — Mitigation: connection pool size increased, query
  identified for indexing fix in follow-up.
- 15:19:12 — Impact confirmed resolved; incident closed.

## Impact
Elevated 5xx error rate on /checkout, peaking at 8% of requests, for
47 minutes. Estimated 3,200 failed checkout attempts.

## Contributing factors
1. A recent schema migration omitted an index specified in the original
   migration plan.
2. No automated post-migration check verifies planned indexes exist.
3. Connection pool had no circuit breaker to fail fast and preserve
   partial capacity under exhaustion.
4. The pool-exhaustion symptom was not covered in the existing runbook,
   costing roughly 8 minutes of otherwise-avoidable diagnostic time.

## What went well
- Burn-rate alert (Chapter 03) caught the degradation within the
  5-minute short window as designed.
- Major incident declared promptly once ambiguity exceeded the
  threshold, avoiding a longer solo-diagnosis delay.

## Action items
| Item | Owner | Tracking | Target date |
| --- | --- | --- | --- |
| Add missing index (PRB-0091 / CHG-2026-0714) | @carmen | JIRA-4471 | 2026-07-20 |
| Add automated post-migration index verification gate | @bao | JIRA-4472 | 2026-08-01 |
| Add circuit breaker to checkout-api's DB connection pool | @alice | JIRA-4473 | 2026-08-15 |
| Update runbook with pool-exhaustion diagnostic steps | @alice | JIRA-4474 | 2026-07-22 |
```

## Validation and Troubleshooting

- **Audit for incidents closed without a linked postmortem.** Query the
  incident tracker for every SEV1/SEV2 incident in the last quarter and
  confirm each has a linked postmortem record; a gap here is a process
  failure worth surfacing to leadership directly, since it represents
  systematically lost learning.
- **Audit for stale problem records.** A problem record open for months
  with no update is either genuinely low priority (and should be
  explicitly deprioritized and documented as an accepted risk, closing
  the ambiguity) or has silently stalled; review the problem backlog on
  a fixed cadence rather than only when a recurrence forces attention
  back to it.
- **Symptom: the same incident signature recurs despite a "completed"
  postmortem action item.** Confirm the action item actually addressed a
  genuine contributing factor rather than a symptom-level workaround
  that was marked complete without closing the underlying gap — this is
  a common failure when action item completion is tracked as a checkbox
  rather than verified against the original contributing factor it was
  meant to resolve.
- **Symptom: emergency changes trending upward as a fraction of total
  changes.** This is a leading indicator that either genuine incident
  volume is rising (a problem-management concern) or that teams are
  misclassifying normal changes as emergency to bypass approval
  friction (a change-governance concern); investigate which, since the
  interventions differ completely.
- **Change record exists but deployment bypassed the gate.** Confirm the
  CI/CD pipeline's approval gate (the script above, or equivalent) is
  actually wired into the deployment path used in practice, not only
  into a documented "intended" path — a manual `kubectl apply` or a
  secondary deploy mechanism that does not invoke the gate is a common
  and serious governance gap discovered only during an audit or, worse,
  during an incident caused by an unapproved change.

## Security and Best Practices

- Treat the change record as an auditable control, not paperwork:
  regulatory frameworks referenced in [Volume X](../../volume-10-enterprise-cybersecurity/README.md) (PCI DSS, SOX,
  ISO 27001) commonly require demonstrable evidence that production
  changes were reviewed and approved before deployment, and a change
  management process that exists in documentation but is not actually
  enforced at the deployment gate does not satisfy that requirement
  under audit scrutiny.
- Protect postmortem documents' blameless intent structurally: restrict
  their use in performance review processes by policy, since any
  perceived connection between postmortem contribution and individual
  performance evaluation reliably and quickly ends candid incident
  reporting.
- Require every emergency change to be retrospectively reviewed by the
  standard change approval body (Chapter Advisory Board equivalent)
  within a defined window (commonly 24-48 hours), so the expedited path
  remains accountable after the fact even though it bypasses prior
  approval.
- Restrict who can mark an incident resolved or a major incident stood
  down to the incident commander role for that incident, not any
  participant, to prevent a premature or inaccurate close that
  understates real impact or leaves a mitigation incomplete.
- Log all change-record and postmortem-system access and modification
  events; these systems collectively document what changed in
  production, why, and what went wrong, making them a high-value
  target and a key evidentiary source during a security investigation
  as well as an operational one.

## References and Knowledge Checks

**References**

- AXELOS/PeopleCert, *ITIL 4 Foundation*, practices for Incident
  Management, Problem Management, and Change Enablement.
- Google, *Site Reliability Engineering*, Chapter 15 ("Postmortem
  Culture: Learning from Failure"), free online edition.
- Allspaw, J., "Blameless PostMortems and a Just Culture" (Etsy
  engineering blog), for the foundational blameless-postmortem argument.
- PagerDuty, *Incident Response Documentation*, for incident commander
  and major-incident role definitions referenced in this chapter.

**Knowledge Checks**

1. Explain, using the definitions in this chapter, why "the fix worked
   and service was restored" is a valid incident management outcome even
   without a known root cause, and why that is not sufficient on its
   own.
2. What three roles compose a major incident command structure, and why
   are they deliberately assigned to different people rather than
   combined?
3. Contrast the Five Whys technique with a contributing-factors model
   and explain a limitation of relying on the Five Whys alone.
4. Why must an emergency change still be recorded and reviewed
   retrospectively even though it bypasses prior approval?
5. Describe a structural safeguard (not a policy statement alone) that
   protects a blameless postmortem process from being used in individual
   performance evaluation.

## Hands-On Lab

**Objective:** Build a lightweight, file-based incident and change
record workflow with an automated postmortem-completeness audit and a
change-approval gate, and validate both the compliant and
non-compliant paths.

### Prerequisites

- A POSIX shell (bash 5.x) and `yq` (Mike Farah's Go implementation,
  v4.x) installed locally.
- No production access required; this lab is entirely local files.

### Procedure

1. Create the lab directory structure:

   ```bash
   mkdir -p ~/svcmgmt-lab/incidents ~/svcmgmt-lab/postmortems ~/svcmgmt-lab/changes
   cd ~/svcmgmt-lab
   ```

2. Create two incident records, one SEV1 and one SEV3, and one
   postmortem linked to the SEV1:

   ```bash
   cat > incidents/INC-1001.yaml <<'EOF'
   incident_id: INC-1001
   severity: SEV1
   service: checkout-api
   status: resolved
   EOF

   cat > incidents/INC-1002.yaml <<'EOF'
   incident_id: INC-1002
   severity: SEV3
   service: inventory-service
   status: resolved
   EOF

   cat > postmortems/INC-1001.yaml <<'EOF'
   incident_id: INC-1001
   contributing_factors:
     - Missing index after schema migration
     - No circuit breaker on DB connection pool
   action_items:
     - owner: alice
       ticket: JIRA-4473
       status: open
   EOF
   ```

3. Save the `require-change-approval.sh` script from the Implementation
   and Automation section, make it executable, and create one fully
   approved `normal` change and one under-approved one:

   ```bash
   chmod +x require-change-approval.sh

   cat > changes/CHG-2001.yaml <<'EOF'
   change_id: CHG-2001
   risk_category: normal
   approvals:
     - approver: team-lead
       status: approved
     - approver: dba-team
       status: approved
   EOF

   cat > changes/CHG-2002.yaml <<'EOF'
   change_id: CHG-2002
   risk_category: normal
   approvals:
     - approver: team-lead
       status: approved
   EOF
   ```

4. Create the postmortem-completeness audit script:

   ```bash
   cat > audit-postmortem-coverage.sh <<'EOF'
   #!/usr/bin/env bash
   set -euo pipefail
   missing=0
   for f in incidents/*.yaml; do
     id=$(yq '.incident_id' "$f")
     sev=$(yq '.severity' "$f")
     if [[ "$sev" == "SEV1" || "$sev" == "SEV2" ]]; then
       if [[ ! -f "postmortems/${id}.yaml" ]]; then
         echo "MISSING POSTMORTEM: $id ($sev)"
         missing=$((missing + 1))
       fi
     fi
   done
   echo "Postmortem coverage audit complete: $missing issue(s) found"
   exit "$missing"
   EOF
   chmod +x audit-postmortem-coverage.sh
   ```

5. Run both audits:

   ```bash
   ./audit-postmortem-coverage.sh
   echo "--- change gate: CHG-2001 ---"
   ./require-change-approval.sh changes/CHG-2001.yaml && echo "exit: $?"
   echo "--- change gate: CHG-2002 ---"
   ./require-change-approval.sh changes/changes/CHG-2002.yaml 2>/dev/null || echo "exit: $?"
   ```

### Expected Results

The postmortem audit reports `0 issue(s) found`, since `INC-1001` (SEV1)
has a linked postmortem and `INC-1002` (SEV3) does not require one. The
change gate for `CHG-2001` prints `Change CHG-2001 approved; proceeding.`
and exits `0`. The change gate for `CHG-2002` (correct the path to
`changes/CHG-2002.yaml`) prints a `BLOCKED` message reporting `1/2`
approvals and exits non-zero.

### Negative Test

Remove the postmortem for `INC-1001` to simulate an incident closed
without one, and confirm the audit now catches it:

```bash
mv postmortems/INC-1001.yaml postmortems/INC-1001.yaml.bak
./audit-postmortem-coverage.sh || echo "exit code: $?"
```

Confirm the script reports `MISSING POSTMORTEM: INC-1001 (SEV1)` and
exits non-zero, demonstrating the gate would fail a CI check on this
condition rather than silently allowing a SEV1 incident to close without
a postmortem. Restore the file (`mv postmortems/INC-1001.yaml.bak
postmortems/INC-1001.yaml`) and confirm the audit passes again.

### Cleanup

```bash
cd ~
rm -rf ~/svcmgmt-lab
```

## Summary and Completion Checklist

Incident management restores service fast without requiring root cause;
problem management deliberately follows to find and fix root cause,
using techniques from the Five Whys to a fuller contributing-factors
model, informed by a blameless postmortem that produces tracked action
items rather than narrative alone; change management is the preventive
practice that reduces how often a deliberate modification becomes the
next incident. The major incident command structure — separate
incident commander, operations lead, and communications lead roles —
scales response to genuinely large or ambiguous incidents without
overloading any single responder. [Chapter 08](08-capacity-performance-and-cost-aware-operations.md) turns from incident
response to the proactive side of operations: capacity, performance, and
cost-aware planning that reduces how often these processes are needed at
all.

**Completion checklist**

- [ ] Can distinguish incident, problem, and change management by the
      question each answers and the timescale each operates on.
- [ ] Can describe the major incident command structure and why its
      three roles are assigned to different people.
- [ ] Can write a blameless postmortem with contributing factors and
      tracked, owned action items.
- [ ] Can classify a change by risk category and route it through the
      correct approval path.
- [ ] Built and validated a working postmortem-coverage audit and a
      change-approval gate, including a negative test for each.
