# Chapter 7: Recovery Engineering and Disaster Recovery Validation

## Learning Objectives

- Compare cold, warm, hot, and active-active DR site models on RTO, cost,
  and operational complexity.
- Decompose RTO into detection, decision, and execution phases and
  identify which phase most commonly dominates real recovery time.
- Structure a recovery runbook with trigger criteria, roles, step-by-step
  procedures, and validation checkpoints.
- Explain why failback is frequently riskier than failover and design a
  failback procedure that accounts for data written during the outage.
- Compare DR test types — tabletop, structured walkthrough, simulation,
  parallel test, and full interruption test — and select an appropriate
  cadence per service tier.
- Execute a recovery test, measure actual RTO against target, and validate
  recovered data currency against RPO.
- Diagnose common DR test failures and runbook gaps.

## Theory and Architecture

[Chapter 5](05-backup-architecture-and-data-protection-policy.md) built the mechanisms that limit data loss (backup) and [Chapter 6](06-snapshots-replication-and-continuous-data-protection.md)
built the mechanisms that limit it further and enable site-to-site copies
(snapshots and replication). Recovery engineering is the discipline that
turns those mechanisms into an actual, working, *timed* recovery — the
difference between "we have a replica" and "we can be running again in
under two hours, and we know that because we have measured it."

### DR site models

| Model | Infrastructure readiness | Data currency | Typical RTO | Relative cost |
| --- | --- | --- | --- | --- |
| Cold | No standby infrastructure provisioned; hardware/capacity acquired or repurposed at time of disaster | Restored from backup ([Chapter 5](05-backup-architecture-and-data-protection-policy.md)) | Days | Lowest |
| Warm | Infrastructure provisioned but scaled down or not running; data kept reasonably current via periodic replication or restore | Hours to a day behind, depending on replication schedule | Hours | Moderate |
| Hot | Infrastructure fully provisioned and running (or ready to start immediately); data kept current via continuous replication ([Chapter 6](06-snapshots-replication-and-continuous-data-protection.md)) | Minutes behind (asynchronous) to zero (synchronous) | Minutes to low hours | High |
| Active-active | Both sites fully live and serving production traffic simultaneously | Continuous, bidirectional | Near-zero — a site loss is absorbed by the surviving site with minimal disruption | Highest |

These models sit on a well-established cost curve: each step toward a
lower RTO costs disproportionately more than the previous step, because it
requires progressively more standing infrastructure, more continuous data
movement, and more operational sophistication (conflict resolution for
active-active, per [Chapter 6](06-snapshots-replication-and-continuous-data-protection.md)) running at all times rather than only during
a disaster. The correct model for a given workload is the one that matches
its RTO requirement from the service catalog ([Chapter 1](01-enterprise-storage-architecture-and-service-design.md)) at the lowest cost
that still meets it — a Platinum-tier database justifies a hot or active-
active model; a Bronze-tier file share rarely does.

### Decomposing RTO

RTO is not a single technical number; it is the sum of three phases, and
organizations that measure only the fastest one systematically
underestimate their real recovery time:

1. **Detection time** — the time between the failure occurring and the
   organization becoming aware of it. Driven entirely by monitoring and
   alerting maturity ([Chapter 9](09-storage-automation-observability-capacity-and-lifecycle-operations.md)); a failure that is not detected for 40
   minutes has already consumed 40 minutes of whatever RTO budget exists,
   regardless of how fast the technical failover itself runs.
2. **Decision time** — the time between detection and a formal decision to
   invoke disaster recovery. This is consistently the most underestimated
   and most variable phase in real incidents: it depends on human judgment,
   escalation paths, and organizational authority to declare a disaster,
   not on technology. A team without pre-defined trigger criteria and
   pre-delegated authority to invoke DR routinely loses more time here than
   in the entire technical execution phase combined.
3. **Execution time** — the actual technical work: promoting a replica,
   starting or scaling compute, redirecting traffic (DNS or load-balancer
   pool changes), starting application services in dependency order, and
   validating the result. This is the phase most DR tooling and automation
   ([Chapter 9](09-storage-automation-observability-capacity-and-lifecycle-operations.md)) is built to accelerate — and the phase most DR test programs
   focus on exclusively, which is precisely why decision time is so often
   the unmeasured, unmanaged risk in an actual event.

```text
Total RTO = Detection time + Decision time + Execution time
```

Reducing detection time is an observability investment. Reducing decision
time is a governance and pre-authorization investment — defining, in
advance, exactly what conditions trigger a declared disaster and who has
standing authority to declare it, so the decision does not have to be
invented live during the incident. Reducing execution time is where
runbooks, orchestration, and rehearsal (the remainder of this chapter)
concentrate their value.

### Recovery runbooks

A recovery runbook is the authoritative, tested procedure for executing a
recovery. A usable runbook contains, at minimum:

- **Trigger criteria** — the specific, objective conditions under which
  this runbook should be invoked, reducing decision time by removing
  ambiguity about whether a given situation qualifies.
- **Roles and authority** — who is authorized to declare the disaster and
  invoke the runbook (an Incident Commander role is common), and who
  executes each technical step, so execution does not stall waiting for
  someone to volunteer or seek permission mid-incident.
- **Step-by-step procedure** — exact commands, not general guidance;
  a runbook that says "fail over the database" is not a runbook, it is a
  reminder that a runbook needs to be written.
- **Validation checkpoints** — explicit checks after each major step
  confirming it succeeded before proceeding to the next, so a failure at
  step 3 is caught at step 3, not discovered as a mystery at step 9.
- **Communication plan** — who is notified, on what channel, at what
  points in the process.
- **Failback procedure** — a fully separate, equally detailed procedure
  for returning to the original primary site once it is available again
  (see below).

A runbook that has never been executed against the real environment is an
untested assumption, identical in kind to the untested backup from Chapter
5 — and for the same reason: infrastructure drifts (hostnames change, IP
ranges are re-addressed, a dependency is added without updating the
runbook) and a runbook that was accurate a year ago is not guaranteed to
be accurate today. Runbooks require version control, an owner, and a
review/test cadence, not a one-time authoring effort.

### Failover and the underappreciated risk of failback

**Failover** is the act of promoting a secondary/replica environment to
primary and redirecting production traffic to it. **Failback** is the
reverse: returning to the original primary once it has been restored or
repaired. Failover tends to receive the design and testing attention;
failback is frequently treated as "just do the same thing in reverse,"
which is a dangerous assumption for one specific reason — **data written
at the DR site during the outage window must be reconciled back to the
original primary**, and naively reversing the replication direction risks
silently overwriting or losing that data. A well-executed failover
followed by a careless failback is a well-documented pattern for turning a
successful recovery into a second, self-inflicted data-loss incident. A
complete recovery runbook treats failback as a first-class procedure with
its own reconciliation step, not an afterthought appended to the failover
plan.

### DR test types

| Test type | What happens | Production risk | What it validates |
| --- | --- | --- | --- |
| Tabletop exercise | Discussion-based walkthrough of the plan; no systems touched | None | Roles, communication plan, and whether the plan makes sense on paper |
| Structured walkthrough | Technical team walks through the runbook's exact steps against the real environment, without executing destructive actions | Minimal | Whether the runbook's specific commands, hostnames, and references are still accurate |
| Simulation test | Recovery is executed in an isolated/sandboxed copy of the environment | None to production | Whether the technical procedure actually works end to end, without touching production |
| Parallel test | The DR environment is brought fully live in parallel with production, which continues running untouched | None to production, some cost/complexity | Whether the DR environment can actually run the workload for real, side by side with production |
| Full interruption test | Production traffic is actually cut over to the DR site | Highest — a real outage if the test fails | The complete, real, end-to-end recovery experience including actual traffic cutover |

Test cadence and depth should scale with service tier: a Bronze-tier
workload may only warrant an annual tabletop exercise, while a Platinum-
tier workload justifies periodic full interruption tests precisely because
that is the only test type that validates the actual cutover mechanism
(DNS/load-balancer changes, certificate validity at the DR site, and every
dependency) under real conditions. A recovery test program that only ever
performs tabletop exercises for a tier-1 workload has not actually
validated its stated RTO — it has validated that the plan is plausible on
paper.

## Design Considerations

- **Match DR site model to service tier**, not to what is easiest to build;
  an over-built DR model for a low tier wastes budget the organization
  could spend closing a real gap elsewhere, and an under-built model for a
  high tier is a silent risk that will surface at the worst possible time.
- **Invest in decision-time reduction deliberately.** Predefined,
  objective trigger criteria and pre-delegated declaration authority
  usually produce a larger RTO improvement than any additional technology
  spend, because decision time is frequently the largest, least-managed
  component of real-world RTO.
- **Map application dependencies completely** before designing a recovery
  procedure — DNS, TLS certificates, license servers, downstream
  integration endpoints, and authentication providers all have to be
  reachable and valid at the DR site, and a recovery test that only
  exercises storage and compute will not catch a missing dependency until
  a real event does.
- **Design failback as a first-class procedure**, including an explicit
  data-reconciliation step for anything written at the DR site during the
  outage window.
- **Scale test type and cadence to service tier**, reserving full
  interruption tests for the workloads whose RTO claim genuinely needs
  that level of validation, and using lower-risk test types more frequently
  for everything else.
- **Store the runbook somewhere reachable during the actual failure it
  describes.** A runbook stored exclusively on a system, wiki, or
  authentication provider that could itself be part of the outage is a
  design flaw discovered at the worst possible time; maintain an offline
  or independently hosted copy.

## Implementation and Automation

### Runbook structure (as a version-controlled artifact)

```yaml
# dr-runbook-tier1-database.yaml
service: tier1-database
trigger_criteria:
  - "Primary site unreachable for > 5 minutes, confirmed by two independent monitoring sources"
  - "Primary storage array reports unrecoverable hardware failure"
declaration_authority:
  - role: incident_commander_on_call
decision_time_target_minutes: 10
roles:
  incident_commander: "pages on-call rotation: dr-ic"
  storage_lead: "promotes replication target, validates data currency"
  application_lead: "starts application services in dependency order"
  network_lead: "executes DNS/load-balancer cutover"
procedure:
  - step: 1
    action: "Confirm trigger criteria met; declare disaster"
    owner: incident_commander
    validation: "Incident ticket opened, all leads paged"
  - step: 2
    action: "Promote replication target to read/write at DR site"
    owner: storage_lead
    command: "replication relationship promote RR_DB01_DATA --target-site site-b"
    validation: "Target volume reports read/write; replication relationship shows 'failed over'"
  - step: 3
    action: "Start database service at DR site"
    owner: application_lead
    command: "systemctl start postgresql"
    validation: "Database accepts connections; replay of WAL completes without error"
  - step: 4
    action: "Redirect application traffic to DR site"
    owner: network_lead
    command: "Update DNS record app-db.example.com to DR site VIP; confirm propagation"
    validation: "Client connections resolve to DR site; application health check passes"
failback_procedure:
  - step: 1
    action: "Confirm original primary site is repaired and reachable"
    owner: storage_lead
  - step: 2
    action: "Reconcile data written at DR site during the outage window back to primary before resuming replication in the original direction"
    owner: storage_lead
    validation: "Explicit diff/reconciliation report reviewed and approved before any bulk data copy runs"
  - step: 3
    action: "Re-establish replication from primary to DR site in the original direction"
    owner: storage_lead
  - step: 4
    action: "Redirect traffic back to primary during a scheduled change window"
    owner: network_lead
```

Note that the failback procedure's step 2 is deliberately explicit about
reconciliation happening *before* any bulk copy — this is the exact control
that prevents the failback data-loss pattern described in the theory
section.

### Illustrative recovery orchestration (sequencing)

```yaml
# Illustrative orchestration sequence — generic pattern, engine-agnostic
- name: Execute tier-1 database failover
  tasks:
    - name: Record failover start timestamp
      shell: "date -u +%FT%TZ >> /var/log/dr-failover-timeline.log"
    - name: Promote storage replication target
      command: "replication relationship promote RR_DB01_DATA --target-site site-b"
    - name: Wait for target volume to report read/write
      until_state: "read_write"
      timeout_seconds: 120
    - name: Start database service
      service: { name: postgresql, state: started }
    - name: Validate database connectivity
      command: "pg_isready -h localhost -p 5432"
      retries: 10
      delay_seconds: 5
    - name: Update DNS record for application traffic
      dns_record:
        name: app-db.example.com
        value: "{{ dr_site_vip }}"
        ttl: 60
    - name: Record failover completion timestamp
      shell: "date -u +%FT%TZ >> /var/log/dr-failover-timeline.log"
```

Recording explicit start/completion timestamps around the execution phase,
as shown above, is what makes RTO a measured fact rather than an assumed
one — [Chapter 9](09-storage-automation-observability-capacity-and-lifecycle-operations.md) builds this into ongoing observability, but every recovery
test should produce this timeline as a baseline artifact.

## Validation and Troubleshooting

| Symptom | Likely cause | Diagnostic step |
| --- | --- | --- |
| Recovery test takes far longer than the target RTO | Decision-time delay not accounted for in prior estimates, or a runbook step referencing stale infrastructure | Break the measured time into detection/decision/execution and compare each against the design assumption |
| Runbook step fails because a referenced host/IP no longer exists | Infrastructure drift since the runbook was last validated | Update the runbook immediately and schedule a structured walkthrough to catch further drift |
| Application starts at DR site but cannot reach a dependency | Incomplete dependency mapping (DNS, certificate authority, license server, downstream API) | Re-map the application's full dependency graph and add missing components to the runbook and DR site build |
| DR site traffic cutover takes much longer than expected | High DNS TTL on the production record, or an application with a hard-coded IP address rather than an FQDN | Lower TTL well in advance of any anticipated cutover; audit for hard-coded IP references |
| Failback introduces data loss or conflicts | Replication direction reversed without reconciling DR-site writes made during the outage | Halt the failback, restore from the last known-consistent point, and rebuild the failback procedure with an explicit reconciliation step |
| Full interruption test itself causes an unplanned outage | Untested runbook step, insufficient rollback plan for the test itself | Always define and rehearse an abort/rollback path for the test before executing a full interruption test |

## Security and Best Practices

- Apply the same security posture to the DR site as the primary site —
  access control, patching, and monitoring; a DR site that is a security
  soft spot undermines the resilience it exists to provide ([Chapter 8](08-storage-security-ransomware-resilience-and-data-governance.md)
  develops this further).
- Restrict authority to invoke a real failover to the roles explicitly
  named in the runbook, and log every invocation and every execution step
  as an auditable record.
- Store runbooks in a location proven reachable independent of the systems
  the runbook is recovering, including an offline or out-of-band copy.
- Treat every DR test as a change with its own change-control record,
  including a defined abort criterion for full interruption tests.
- Conduct a retrospective after every test (including tabletop exercises),
  track identified gaps to closure, and re-test the specific gap once
  remediated rather than assuming the fix worked.
- Review and re-validate the runbook whenever the protected application's
  architecture changes — a new dependency, a new data volume, or a new
  integration point that is not reflected in the runbook is a recovery gap
  waiting to be discovered during a real incident.

## References and Knowledge Checks

**References**

- NIST SP 800-34 (Contingency Planning Guide for Federal Information
  Systems), the same source underpinning [Chapter 5](05-backup-architecture-and-data-protection-policy.md)'s RPO/RTO definitions.
- [ISO 22301 (Business Continuity Management Systems) for organizational DR
  program structure references.](https://www.iso.org/standard/75106.html)
- [SOFTWARE_VERSIONS.md](../../../SOFTWARE_VERSIONS.md) — dated Linux baseline used for this chapter's
  orchestration and lab examples.

**Knowledge Checks**

1. A DR test measures a 12-minute technical failover against a 2-hour RTO
   target, yet the last real incident took 3 hours to recover from.
   Explain, using the three-phase RTO breakdown, how both facts can be
   true simultaneously.
2. Why is decision time frequently the largest lever for improving real-
   world RTO, and what two design elements most directly reduce it?
3. Describe the specific data-loss risk in a failback procedure that
   simply reverses the original replication relationship without an
   explicit reconciliation step.
4. Compare a structured walkthrough and a parallel test on production risk
   and on what each actually validates.
5. Why does a runbook that has never been executed against the real
   environment carry the same category of risk as an untested backup from
   [Chapter 5](05-backup-architecture-and-data-protection-policy.md)?

## Hands-On Lab

### Lab: Execute and Measure a Simulated Application Failover and Failback

This lab builds a minimal two-site application (a simple web service with
asynchronously replicated data), executes a timed failover following a
written runbook, validates recovered data currency against the last
replication point, and then demonstrates — as a negative test — the data-
loss risk of a careless failback.

**Prerequisites**

- Two Linux hosts (RHEL 10 or Ubuntu Server 26.04 LTS baseline): `app01`
  (primary) and `app02` (DR site), reachable from a third host or your own
  workstation (`client01`) used to validate the application.
- Root or sudo access on `app01` and `app02`.
- `rsync` and Python 3 (for a minimal test web server) installed on both
  `app01` and `app02`.

**Procedure**

1. On `app01`, create the application's data directory and start a simple
   web service:

   ```bash
   sudo mkdir -p /srv/app/data
   echo "PRIMARY (app01) - content version 1" | sudo tee /srv/app/data/index.html
   cd /srv/app/data && sudo python3 -m http.server 8080 &
   ```

2. On `app02`, create a matching directory with placeholder standby
   content and its own listener on a different port (representing the
   not-yet-promoted DR service):

   ```bash
   sudo mkdir -p /srv/app/data
   echo "STANDBY (app02) - not yet promoted" | sudo tee /srv/app/data/index.html
   cd /srv/app/data && sudo python3 -m http.server 8081 &
   ```

3. Simulate asynchronous replication by running `rsync` from `app01` to
   `app02` (in production this step would run continuously or on a fixed
   interval — this is the RPO-defining schedule from [Chapter 6](06-snapshots-replication-and-continuous-data-protection.md)):

   ```bash
   sudo rsync -avz --delete /srv/app/data/ app02:/srv/app/data/
   ```

   **Expected result:** confirm on `app02` that `index.html` now shows
   `PRIMARY (app01) - content version 1`, proving the replica is current
   as of this sync.

4. Create the runbook's timeline log and record the failover trigger:

   ```bash
   date -u +%FT%TZ | tee -a /tmp/dr-failover-timeline.log   # trigger time
   ```

5. Execute the failover: simulate the primary's failure, then promote
   `app02` by writing new "promoted" content and restarting its service to
   represent activation (in a real environment this step promotes storage
   replication and starts the actual application, as shown in the
   Implementation section's runbook):

   ```bash
   # Simulate primary failure
   sudo pkill -f "http.server 8080"

   # On app02: promote to active
   echo "PROMOTED - now serving as primary (app02)" | sudo tee -a /srv/app/data/index.html
   date -u +%FT%TZ | tee -a /tmp/dr-failover-timeline.log   # execution complete
   ```

6. Validate from `client01` (or from `app02` itself) that the DR site is
   now serving traffic, and calculate the elapsed execution time from the
   timeline log:

   ```bash
   curl http://app02:8081/index.html
   ```

   **Expected result:** the response includes both the last replicated
   content and the "PROMOTED" line, and the two timestamps in
   `/tmp/dr-failover-timeline.log` show the actual execution-phase
   duration — the measured RTO component this lab can realistically
   demonstrate.

**Negative test**

7. While `app02` is serving as primary, write new data representing
   activity during the outage window, then perform a careless failback by
   reversing the `rsync` direction without reconciliation:

   ```bash
   # New data written at the DR site during the outage
   echo "NEW ORDER RECORD created during outage window" | sudo tee -a /srv/app/data/index.html

   # Careless failback: naive rsync back to the original primary,
   # overwriting whatever app01 has without checking for conflicts
   sudo rsync -avz --delete app02:/srv/app/data/ /srv/app/data/   # run on app01
   ```

   **Expected result:** inspect `/srv/app/data/index.html` on `app01`
   afterward — the file now reflects only `app02`'s final state. If
   `app01` had also accumulated any independent local change after the
   simulated failure (for example, a manual recovery attempt before DR was
   declared), this naive reversal would have silently discarded it with no
   warning and no conflict report, which is precisely the failback risk
   described in this chapter's theory section. A correct failback instead
   requires an explicit diff/reconciliation step before any bulk copy, as
   shown in the runbook example.

**Cleanup**

8. Stop both web services and remove the lab data and timeline log:

   ```bash
   sudo pkill -f "http.server 8081" || true
   sudo rm -rf /srv/app/data
   rm -f /tmp/dr-failover-timeline.log
   ```

   Run the equivalent cleanup on both `app01` and `app02`.

## Summary and Completion Checklist

This chapter covered DR site models and their RTO/cost trade-offs, the
three-phase decomposition of RTO (detection, decision, execution), recovery
runbook structure, the underappreciated data-reconciliation risk in
failback, and the spectrum of DR test types from tabletop exercise to full
interruption test. It then executed a timed, runbook-driven failover and
demonstrated the failback data-loss risk directly through a negative test.

**Completion checklist**

- [ ] Can compare cold, warm, hot, and active-active DR models on RTO and
      cost.
- [ ] Can decompose RTO into detection, decision, and execution phases and
      explain which typically dominates real recovery time.
- [ ] Has structured a recovery runbook with trigger criteria, roles,
      validation checkpoints, and a separate failback procedure.
- [ ] Can explain why failback requires explicit data reconciliation.
- [ ] Can compare DR test types and select an appropriate cadence per
      service tier.
- [ ] Has executed and timed a simulated failover against a written
      runbook.
- [ ] Has reproduced the failback data-loss risk through a negative test.
