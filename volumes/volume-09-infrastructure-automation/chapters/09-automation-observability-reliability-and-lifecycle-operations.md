# Chapter 09: Automation Observability, Reliability, and Lifecycle Operations

![Lab flow for this chapter: a wrapper script around terraform apply records run_id, duration, exit_status, and timestamp as one JSON line per run; three successful runs produce a computed success rate of 3/3. Separately, a Vault dev-mode backup-and-restore drill seeds a marker secret to prove a backup is actually usable, not merely present. As a negative test, a deliberately broken resource is added and the wrapper run a fourth time; the run log gains a fourth entry with a non-zero exit_status, and the recomputed success rate correctly drops to 3/4 — proving the instrumentation captures failures as data instead of only recording successful runs.](../../../diagrams/volume-09-infrastructure-automation/chapter-09-structured-logging-success-rate-flow.svg)

*Figure 9-1. Flow used throughout this chapter's Hands-On Lab: structured JSON logging around Terraform apply feeding a success-rate metric that correctly captures a failed run.*

## Learning Objectives

- Apply the three observability pillars (logs, metrics, traces) to the
  automation control plane itself, not just the infrastructure it manages.
- Define and measure automation-specific reliability indicators: pipeline
  success rate, mean time to recovery, and drift frequency.
- Emit structured logs and pipeline metrics from Terraform and Ansible runs
  and alert on regressions without causing alert fatigue.
- Design backup and restore procedures for Terraform state, Vault, and
  Ansible Automation Platform.
- Apply a deprecation policy to shared modules, roles, and collections
  across their lifecycle.
- Diagnose automation reliability failures: missing metrics, alert noise,
  and failed restore drills.

## Theory and Architecture

Every chapter in this volume has built a piece of an automation control
plane: state backends and modules ([Chapter 02](02-infrastructure-as-code-state-providers-and-modules.md)), configuration management
([Chapter 03](03-configuration-management-and-desired-state-convergence.md)), integrations ([Chapter 04](04-api-event-and-integration-automation.md)), pipelines ([Chapter 05](05-automation-pipelines-testing-and-policy-gates.md)), identity
and secrets ([Chapter 06](06-automation-identity-secrets-and-privileged-execution.md)), orchestration ([Chapter 07](07-workflow-orchestration-and-event-driven-operations.md)), and supply-chain
integrity ([Chapter 08](08-automation-security-governance-and-supply-chains.md)). This closing chapter treats that whole control
plane as what it actually is — a production system with its own
reliability requirements, not an implementation detail sitting quietly
underneath the infrastructure it manages. [Chapter 03](03-configuration-management-and-desired-state-convergence.md) named this gap
directly: Ansible Automation Platform's job history and centralized
logging are "the enterprise-scale mechanism" for auditing playbook runs,
and this chapter is where that mechanism is built out in full, alongside
its Terraform and pipeline equivalents.

### Why the automation control plane needs its own observability

An outage in application infrastructure is visible immediately — users
notice. An outage or silent failure in the automation control plane is
not: a pipeline that has been failing every run for three days produces no
user-facing symptom until someone needs to make a change and cannot, or
until configuration drift accumulates far enough to cause its own
incident. Automation observability exists specifically to surface that
class of silent failure before it becomes a change-freeze or an incident.

### The three pillars, applied to automation

- **Logs.** Structured, queryable records of what a pipeline stage,
  playbook run, or orchestration workflow did — not just whether it
  succeeded, but which resources changed, which policy rules were
  evaluated ([Chapter 05](05-automation-pipelines-testing-and-policy-gates.md)), and which identity executed it ([Chapter 06](06-automation-identity-secrets-and-privileged-execution.md)).
- **Metrics.** Numeric time series describing the automation system's
  behavior over time: pipeline duration, success/failure rate, time between
  a merge and a completed apply, number of drifted resources detected per
  scheduled `terraform plan`.
- **Traces.** For a multi-step workflow ([Chapter 07](07-workflow-orchestration-and-event-driven-operations.md)) spanning several
  systems, a trace ties the diagnose/approve/remediate steps of a single
  logical operation together, so a failure in one step is visible in the
  context of the whole operation rather than as an isolated, hard-to-
  correlate log line.

[Volume XI](../../volume-11-observability-enterprise-operations/README.md) (Observability and Enterprise Operations) covers these pillars
in general depth; this chapter applies them specifically to the automation
systems this volume has built.

### Reliability indicators for automation

Treat the automation control plane's own reliability with the same SLO
discipline [Volume I, Chapter 06](../../volume-01-enterprise-engineering-foundations/chapters/06-understanding-enterprise-infrastructure.md) introduced for infrastructure services:

| Indicator | What it measures | Why it matters |
| --- | --- | --- |
| Pipeline success rate | Percentage of pipeline runs that complete without failure | A sustained drop signals a systemic problem (a broken shared module, an expired credential) rather than isolated bad changes |
| Mean time to recovery (MTTR) | Time from a pipeline or automation failure to a passing re-run | Long MTTR on automation itself blocks every change behind it, compounding the original problem |
| Drift frequency | Rate at which scheduled `terraform plan` runs detect unmanaged changes | Rising drift frequency indicates a governance gap — changes are reaching production outside the pipeline |
| Time-to-apply | Elapsed time from merge to completed, approved apply | A proxy for how much friction the pipeline itself adds to a well-formed, low-risk change |

### Automation lifecycle operations

Shared modules, roles, and collections have a lifecycle of their own,
mirroring the general infrastructure lifecycle from [Volume I, Chapter 08](../../volume-01-enterprise-engineering-foundations/chapters/08-infrastructure-lifecycle-management.md):
introduced, actively maintained, deprecated, and retired. A module used by
forty root configurations across an organization cannot simply be deleted
or breaking-changed the way a single team's private script can — its
lifecycle needs the same deliberate change management as the
infrastructure it provisions.

## Design Considerations

### What to measure, deliberately

Instrument what informs a decision, not everything that is easy to
collect. Pipeline success rate and time-to-apply directly inform whether
the pipeline itself needs investment; a raw count of `terraform apply`
invocations does not, on its own, inform anything. Start from the
reliability indicators above and add metrics only when a specific question
("why did last week's applies take twice as long?") cannot be answered
with what already exists.

### Avoiding automation alert fatigue

An automation control plane that pages on every single pipeline failure —
including failures caused by a legitimately broken change that a human
author will see directly in their own pull request — trains responders to
ignore the alert channel. Alert on the aggregate signal (success rate
dropping below a threshold over a rolling window, MTTR trending up) rather
than on every individual run failure, and route individual run failures to
the author through the CI platform's own notification, not a shared
on-call channel.

### Backup and disaster recovery for the control plane itself

Every stateful component this volume introduced needs its own backup and
restore plan, because losing it does not just lose data — it removes the
organization's ability to manage its own infrastructure:

- **Terraform state.** Backend versioning ([Chapter 02](02-infrastructure-as-code-state-providers-and-modules.md)) is the primary
  control; test that a prior state version can actually be restored, not
  just that versioning is enabled.
- **Vault.** Regular, encrypted snapshots of Vault's storage backend;
  restoring a Vault snapshot restores every AppRole, policy, and (for the
  KV engine) stored secret as of the snapshot time, but dynamic secrets
  issued after the snapshot are lost and must be reissued.
- **Ansible Automation Platform.** Its own database backup (job history,
  credentials store, inventories, schedules) using its documented backup
  playbook, run on a schedule and tested with an actual restore, not
  merely confirmed to complete without error.

A backup that has never been restored is a hypothesis, not a control —
this chapter's Hands-On Lab specifically exercises a restore, not just a
backup.

### Module and role deprecation policy

Define, in writing, what happens across a shared module or role's
lifecycle: how a breaking change is communicated (a major version bump
plus a changelog entry, at minimum), how long a deprecated version
continues to receive security fixes before retirement, and how consumers
are identified and notified before a version is actually removed from the
registry or mirror. A module with forty consumers and no deprecation
policy either never changes (stagnation) or breaks consumers without
warning (an incident) — a written policy is what allows it to evolve
safely.

### Capacity planning for the control plane

CI runners, Vault clusters, and Ansible Automation Platform execution
nodes are themselves capacity-constrained infrastructure. Track queue
depth and job wait time, not just success/failure, as an early indicator
that the control plane needs more capacity before pipeline latency
degrades enough to be reported as an incident by users of the pipeline.

## Implementation and Automation

### Structured logging from a pipeline run

```bash
#!/usr/bin/env bash
# scripts/apply-with-structured-log.sh
set -euo pipefail

RUN_ID="${GITHUB_RUN_ID:-local-$(date +%s)}"
START_EPOCH=$(date +%s)

terraform apply plan.tfout
APPLY_STATUS=$?

END_EPOCH=$(date +%s)
DURATION=$((END_EPOCH - START_EPOCH))

jq -n \
  --arg run_id "$RUN_ID" \
  --arg workspace "${TF_WORKSPACE:-default}" \
  --argjson duration "$DURATION" \
  --argjson status "$APPLY_STATUS" \
  '{
    event: "terraform_apply_completed",
    run_id: $run_id,
    workspace: $workspace,
    duration_seconds: $duration,
    exit_status: $status,
    timestamp: (now | todate)
  }' | tee -a /var/log/automation/apply-runs.jsonl
```

Structured (JSON Lines) output is the deliberate choice here: a plain-text
"Apply completed in 42s" log line is readable by a human once, but a
`duration_seconds` field is queryable across every run, which is what
turns a log into the metrics feeding the time-to-apply indicator.

### Emitting pipeline metrics to Prometheus via a Pushgateway

```yaml
# .github/workflows/terraform-pipeline.yml (excerpt, apply job)
      - name: Push apply metrics
        run: |
          cat <<EOF | curl --data-binary @- \
            http://pushgateway.acme.internal:9091/metrics/job/terraform_apply/workspace/prod
          # TYPE terraform_apply_duration_seconds gauge
          terraform_apply_duration_seconds ${DURATION}
          # TYPE terraform_apply_success gauge
          terraform_apply_success ${APPLY_SUCCESS}
          EOF
```

```yaml
# prometheus/alerts/automation.yml
groups:
  - name: automation-pipeline
    rules:
      - alert: PipelineSuccessRateLow
        expr: |
          avg_over_time(terraform_apply_success[7d]) < 0.9
        for: 1h
        labels:
          severity: warning
        annotations:
          summary: "Terraform apply success rate below 90% over 7 days"

      - alert: DriftDetected
        expr: increase(terraform_plan_drifted_resources_total[1d]) > 0
        for: 5m
        labels:
          severity: info
        annotations:
          summary: "Scheduled plan detected drift in {{ $labels.workspace }}"
```

`PipelineSuccessRateLow` alerts on the seven-day aggregate — the
alert-fatigue guard from Design Considerations — rather than firing on
every individual failed run, while `DriftDetected` intentionally uses a
lower `severity: info` since drift is a signal worth routing to a review
queue, not necessarily a page.

### Ansible callback plugin for centralized job logging

```python
# playbooks/callback_plugins/json_run_log.py
from ansible.plugins.callback import CallbackBase
import json
import time

DOCUMENTATION = """
callback: json_run_log
type: notification
short_description: Emit structured JSON run summaries for centralized logging
"""


class CallbackModule(CallbackBase):
    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = "notification"
    CALLBACK_NAME = "json_run_log"

    def __init__(self):
        super().__init__()
        self.stats_by_host = {}

    def v2_playbook_on_stats(self, stats):
        for host in stats.processed.keys():
            summary = stats.summarize(host)
            record = {
                "event": "ansible_run_summary",
                "host": host,
                "changed": summary["changed"],
                "failures": summary["failures"],
                "unreachable": summary["unreachable"],
                "timestamp": time.time(),
            }
            print(json.dumps(record))
```

```ini
# ansible.cfg
[defaults]
callbacks_enabled = json_run_log
```

Every playbook run now emits one JSON line per host summarizing changed,
failed, and unreachable counts — shippable to any log aggregator without
custom parsing, and directly answering "how many hosts actually changed on
this run" without grepping colorized console output.

### Backing up and restoring Vault

```bash
# Snapshot (run on a schedule, e.g. via a CI cron trigger)
vault operator raft snapshot save /backups/vault/vault-$(date +%Y%m%d-%H%M).snap

# Restore drill (against a disposable, non-production Vault instance)
vault operator raft snapshot restore /backups/vault/vault-20260718-0200.snap
vault status
vault kv get secret/pipeline/db_password
```

Running the restore drill against a disposable instance, and confirming a
known secret is actually present afterward, is what distinguishes a tested
backup from an assumed one.

### A module deprecation notice

```markdown
<!-- modules/network/CHANGELOG.md excerpt -->
## v3.0.0 — Deprecation notice

`variable "azs"` is deprecated as of v3.0.0 and will be removed in v4.0.0
(no earlier than 2026-10-18). Use `variable "availability_zone_count"`
instead, which selects AZs automatically. v2.x continues to receive
security fixes until 2026-10-18. See MIGRATION.md for the upgrade path.
```

A dated removal commitment, a security-fix window for the deprecated
version, and a migration document are the three components that turn
"deprecated" from an ambiguous warning into an actionable, time-bound plan
consumers can schedule against.

## Validation and Troubleshooting

- **Metrics silently stop appearing.** Confirm the pipeline stage that
  pushes metrics runs even on failure (`if: always()` in GitHub Actions),
  not only on success — a metrics gap during an incident is exactly when
  the data is most needed and most likely to be missing if the push step
  is conditioned on the job otherwise succeeding.
- **Alert fires constantly on `DriftDetected` in an environment with
  legitimate manual emergency changes.** This is a governance signal, not
  a tuning problem — investigate why emergency changes are bypassing the
  pipeline before suppressing the alert; suppressing it hides the
  governance gap Design Considerations warned about.
- **Restore drill fails even though backups "complete successfully."**
  This is precisely why restore drills are required, not optional — a
  backup job reporting success only confirms the write succeeded, not that
  the resulting file is a valid, restorable snapshot. Schedule restore
  drills on a recurring cadence, not just after initially setting up
  backups.
- **Structured logs are present but not queryable.** Confirm log lines are
  valid, single-line JSON with no interleaved plain-text output from the
  same process (a common cause: a script writing both a human-readable
  progress line and a JSON summary line to the same stream without a
  distinguishing prefix or separate stream).
- **A deprecated module version is still receiving new consumers.**
  Confirm the module registry or mirror actually surfaces the deprecation
  notice at resolution time (a registry-native deprecation flag, where
  supported) rather than relying solely on a CHANGELOG entry a new
  consumer is unlikely to read before their first `terraform init`.

## Security and Best Practices

- Redact secrets from structured logs and metrics labels with the same
  discipline as pipeline console output (Chapters 04 and 06) — a
  `terraform_apply_completed` JSON log line is just as capable of leaking
  a credential in a stray field as an unredacted console log.
- Restrict access to automation observability dashboards and job history
  to those who need it; pipeline logs frequently contain infrastructure
  topology and configuration detail that is itself sensitive.
- Store Vault and Terraform state backups encrypted at rest, in a location
  with access control independent of the primary systems they back up —
  a backup store with the same blast radius as the system it protects is
  not a real recovery path.
- Set and enforce a retention policy for automation logs, metrics, and job
  history that meets audit requirements without retaining sensitive
  operational detail indefinitely.
- Test restores on a defined cadence (quarterly, at minimum, for
  Vault and Terraform state) and record the result as evidence, the same
  way a technical-review checklist records chapter sign-off.
- Require the same review and approval for a module's breaking-change
  removal as for the infrastructure changes it enables — deprecation is a
  governed change, not a unilateral maintainer decision.

## References and Knowledge Checks

### References

- Google, *Site Reliability Engineering: Monitoring Distributed Systems* —
  <https://sre.google/sre-book/monitoring-distributed-systems/>
- HashiCorp, *Vault Operator Raft Snapshot Commands* —
  <https://developer.hashicorp.com/vault/docs/commands/operator/raft>
- Red Hat, *Ansible Callback Plugins Documentation* —
  <https://docs.ansible.com/projects/ansible/latest/plugins/callback.html>
- Prometheus, *Alerting Rules Documentation* —
  <https://prometheus.io/docs/prometheus/latest/configuration/alerting_rules/>

### Knowledge Checks

1. Why is a silent automation control-plane failure more dangerous, in
   some respects, than a visible infrastructure outage?
2. Name the four automation reliability indicators introduced in this
   chapter and what governance gap a rising drift frequency specifically
   points to.
3. Why does alerting on a seven-day aggregate success rate avoid the
   alert-fatigue problem that alerting on every failed run does not?
4. What does a successful backup job confirm, and what does it not
   confirm, about disaster recovery readiness?
5. What three elements turn a module deprecation notice into an actionable
   plan rather than an ambiguous warning?

## Hands-On Lab

### Objective

Instrument a local Terraform apply with structured JSON logging, compute a
simple rolling success-rate metric from accumulated run logs, and perform
an actual backup-and-restore drill against a local Vault dev instance to
prove the backup is usable, not merely present.

### Prerequisites

- Terraform 1.9.x, `jq`, and `vault` installed locally.
- No cloud account required.

### Steps

1. Create the lab layout and a minimal configuration:

   ```bash
   mkdir -p observability-lab && cd observability-lab
   cat > main.tf <<'EOF'
   terraform {
     required_providers {
       random = { source = "hashicorp/random", version = "~> 3.6" }
     }
   }
   resource "random_pet" "example" {
     length = 2
   }
   EOF
   terraform init
   ```

2. Save the structured-logging wrapper script from the Implementation
   section as `apply-with-log.sh`, adjusted for a local log path:

   ```bash
   cat > apply-with-log.sh <<'EOF'
   #!/usr/bin/env bash
   set -uo pipefail
   RUN_ID="local-$(date +%s)"
   START_EPOCH=$(date +%s)
   terraform apply -auto-approve
   APPLY_STATUS=$?
   END_EPOCH=$(date +%s)
   DURATION=$((END_EPOCH - START_EPOCH))
   jq -n \
     --arg run_id "$RUN_ID" \
     --argjson duration "$DURATION" \
     --argjson status "$APPLY_STATUS" \
     '{event:"terraform_apply_completed", run_id:$run_id, duration_seconds:$duration, exit_status:$status, timestamp:(now|todate)}' \
     | tee -a apply-runs.jsonl
   EOF
   chmod +x apply-with-log.sh
   ```

3. Run the wrapper three times, appending to the run log:

   ```bash
   ./apply-with-log.sh
   ./apply-with-log.sh
   ./apply-with-log.sh
   ```

4. Compute a success rate from the accumulated structured logs:

   ```bash
   jq -s 'map(select(.exit_status == 0)) | length as $ok
          | (input_filename | . )
          ' apply-runs.jsonl 2>/dev/null || true
   TOTAL=$(jq -s 'length' apply-runs.jsonl)
   OK=$(jq -s 'map(select(.exit_status == 0)) | length' apply-runs.jsonl)
   echo "Success rate: ${OK}/${TOTAL}"
   ```

5. Perform a Vault backup-and-restore drill in a separate terminal:

   ```bash
   vault server -dev -dev-root-token-id="root" &
   sleep 2
   export VAULT_ADDR="http://127.0.0.1:8200"
   export VAULT_TOKEN="root"
   vault secrets enable -path=secret kv-v2
   vault kv put secret/lab/marker value="present-before-restore-test"
   ```

### Expected Results

- `apply-runs.jsonl` contains three JSON lines, each with
  `"exit_status": 0` and a `duration_seconds` value.
- Step 4 reports `Success rate: 3/3`.
- Step 5's `vault kv put` succeeds and a subsequent
  `vault kv get secret/lab/marker` shows `value = present-before-restore-test`.

### Negative Test

Simulate a failed apply and confirm it is captured accurately in the run
log rather than silently dropped:

```bash
cat >> main.tf <<'EOF'
resource "random_pet" "broken" {
  length = -1
}
EOF
./apply-with-log.sh   # expect a non-zero exit_status recorded
TOTAL=$(jq -s 'length' apply-runs.jsonl)
OK=$(jq -s 'map(select(.exit_status == 0)) | length' apply-runs.jsonl)
echo "Success rate: ${OK}/${TOTAL}"
```

Confirm the run log now has four entries with the fourth showing a
non-zero `exit_status`, and the recomputed success rate correctly drops to
`3/4` — proving the instrumentation captures failures as data instead of
only recording successful runs, which is the entire point of measuring a
success-rate indicator rather than assuming one.

### Cleanup

```bash
terraform destroy -auto-approve 2>/dev/null || true
# Stop the Vault dev server:
kill %1 2>/dev/null || true
cd .. && rm -rf observability-lab
```

## Summary and Completion Checklist

The automation control plane built across this volume — state and
providers, configuration management, integrations, pipelines, identity,
orchestration, and supply-chain controls — is itself a production system,
and this closing chapter is where it receives the same observability,
reliability measurement, backup/restore discipline, and lifecycle
management this volume has applied to every other kind of infrastructure.
Structured logs and pipeline metrics turn "did the apply work" into
queryable data; pipeline success rate, MTTR, drift frequency, and
time-to-apply give that data a small, deliberate set of indicators worth
alerting on; and a tested — not merely scheduled — backup and restore
process is what actually protects an organization's ability to keep
managing its own infrastructure after a control-plane failure. A written
deprecation policy closes the loop by giving shared modules, roles, and
collections the same managed lifecycle as any other infrastructure asset.

- [ ] Can apply the three observability pillars to an automation control
      plane, not just to application infrastructure.
- [ ] Can name and explain all four automation reliability indicators in
      this chapter.
- [ ] Has emitted structured logs from a Terraform or Ansible run and
      computed a metric from them.
- [ ] Has performed an actual backup-and-restore drill, not only a backup.
- [ ] Can describe the three elements a module deprecation notice needs to
      be actionable.
