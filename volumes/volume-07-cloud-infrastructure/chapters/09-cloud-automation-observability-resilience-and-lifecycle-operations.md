# Chapter 09: Cloud Automation, Observability, Resilience, and Lifecycle Operations

## Learning Objectives

- Design a CI/CD pipeline for infrastructure as code that separates plan
  from apply and enforces review before any change reaches a production
  environment.
- Implement drift detection and reconciliation for infrastructure managed
  as code.
- Design an observability strategy across metrics, logs, and traces for a
  cloud workload, and distinguish monitoring from observability.
- Apply chaos engineering principles to validate resilience assumptions
  before an actual failure tests them.
- Design a cloud resource lifecycle and decommissioning process that
  prevents orphaned, unmanaged resource accumulation.
- Implement a complete drift-detection and remediation pipeline as code
  and validate its behavior against an intentionally drifted resource.

## Theory and Architecture

### Infrastructure-as-code pipeline architecture

Building on the IaC-first operating model established in [Chapter 01](01-cloud-operating-models-and-architecture-foundations.md), a
production-grade infrastructure pipeline separates two distinct
operations with different risk profiles:

- **Plan** — a read-only operation that computes the difference between
  the code-defined desired state and the actual deployed state, producing
  a reviewable diff. Plan requires only read access to the target
  environment and can safely run automatically on every proposed change
  (every pull request), since it makes no modification.
- **Apply** — the operation that actually executes the changes described
  by an approved plan. Apply requires write access to the target
  environment and should run only after the corresponding plan has been
  reviewed and explicitly approved, ideally using a more privileged
  identity than the one used for plan, obtained through the workload
  identity federation pattern from [Chapter 03](03-cloud-identity-access-and-cryptographic-services.md) rather than a standing
  credential.

This separation is what makes infrastructure changes reviewable the same
way application code changes are: a reviewer evaluates the actual
computed diff before it takes effect, not just the source code that
produced it, which catches classes of mistakes (an unintended resource
replacement, an unexpected deletion) that reading the code change alone
would miss.

### Drift detection and reconciliation

Drift is any divergence between the state IaC believes is deployed and
the state actually deployed — caused by a manual console change, an
out-of-band API call, or a provider-side change to a resource's default
behavior. Undetected drift undermines the entire premise of
infrastructure as code: if the deployed state can silently diverge from
the code, the code is no longer an authoritative description of the
environment, and the next `apply` may produce a surprising, unreviewed
change as it reconciles the drift.

Detect drift continuously (a scheduled, read-only `plan` run against every
managed environment, independent of any pending change) rather than only
discovering it the next time someone happens to run a plan for an
unrelated change. Reconcile drift deliberately: for a change made
correctly through an approved emergency process but not yet reflected in
code, update the code to match (import or codify the change) rather than
reverting it; for an unauthorized or accidental change, revert it through
the normal apply pipeline. Treat repeated drift on the same resource as a
process signal — it usually indicates a team is routinely bypassing the
pipeline for a specific class of change, which the pipeline should either
accommodate properly or the bypass should be closed.

### Monitoring vs. observability

Monitoring answers questions defined in advance: a dashboard and a set of
alerts built around known failure modes and known metrics ("is CPU
utilization above 80%," "is the error rate above 1%"). Observability is
the broader property of being able to answer questions *not* anticipated
in advance, by examining the system's actual emitted telemetry —
answering "why is this specific request slow" for a request pattern no
one thought to build a dedicated dashboard for, because the underlying
data (structured logs, traces, high-cardinality metrics) supports
open-ended investigation, not just pre-built views. A mature cloud
operations practice needs both: monitoring for known failure modes with
defined alerting thresholds, and observability so that an unanticipated
failure mode can still be investigated effectively using the same
underlying telemetry.

### The three pillars: metrics, logs, and traces

- **Metrics** — numeric measurements aggregated over time (request rate,
  error rate, latency percentiles, resource utilization). Cheap to store
  and query at scale, well suited to alerting thresholds and long-term
  trend analysis, but lose per-request detail through aggregation.
- **Logs** — discrete, timestamped records of events, ideally structured
  (machine-parseable fields, not free-text) rather than unstructured, so
  they can be filtered, aggregated, and correlated programmatically.
  Structured logging is what makes logs usable as an observability data
  source rather than only a manual debugging aid read one line at a time.
- **Traces** — the record of a single request's path through a
  distributed system, showing time spent in each service and dependency
  call along the way. Traces are what make latency root-cause analysis
  tractable in a distributed, multi-service cloud architecture, where a
  single slow user-facing request might touch a dozen internal service
  calls and any one of them could be the actual cause.

Correlate the three pillars through a shared identifier (commonly a trace
ID propagated through logs and linked from metrics dashboards) so an
engineer investigating an alert can move from "the error-rate metric
crossed its threshold" to "here are the specific structured log entries
and traces for the affected requests" without a manual, time-consuming
correlation step during an incident.

### Chaos engineering and resilience validation

Chaos engineering is the deliberate, controlled practice of injecting
failure into a system to validate that its resilience design (multi-zone
distribution, autoscaling, failover, the composite-availability
assumptions from [Chapter 01](01-cloud-operating-models-and-architecture-foundations.md)) actually behaves as designed, rather than
assuming it does based on the architecture diagram. This is the same
principle applied throughout this volume to backups ([Chapter 06](06-cloud-storage-databases-and-data-services.md),
"validate a restore by testing it") and hybrid/multicloud failover
([Chapter 07](07-hybrid-and-multicloud-architecture.md), "test failover on a schedule"), generalized into a standing
practice: terminate an instance and confirm autoscaling replaces it
within the expected time; simulate a zone failure and confirm traffic
shifts to healthy zones without manual intervention; inject latency into
a dependency call and confirm the calling service's timeout and
circuit-breaker behavior activates as designed rather than cascading the
slowdown upstream. Run chaos experiments against a defined hypothesis
("if zone B fails, traffic shifts to zones A and C within 60 seconds with
no error-rate increase above baseline") so each experiment produces a
clear pass/fail result, not just general observation.

### Resource lifecycle and decommissioning

Every resource created in a cloud environment should have a clear owner,
a clear purpose, and — when its purpose ends — a clear decommissioning
path. Two failure modes recur without deliberate lifecycle management:

- **Orphaned resources** — resources whose original owner has left the
  team, whose original purpose (a test environment, a proof of concept)
  has ended, but which were never explicitly decommissioned and continue
  accruing cost and attack surface indefinitely.
- **Unmanaged resources** — resources created outside the infrastructure-
  as-code pipeline (through console access during an incident, for
  example) that were never imported into code afterward, and so are
  invisible to drift detection, policy evaluation, and the standard
  decommissioning process.

Both failure modes are best addressed the same way: continuous, automated
inventory reconciliation (comparing the actual deployed resource
inventory against what code and tagging metadata claim should exist),
combined with an ownership and expiration convention (every resource
tagged with an owner and, for genuinely temporary resources, an
expiration date) enforced through the same policy-as-code guardrails from
[Chapter 02](02-landing-zones-resource-organization-and-guardrails.md).

## Design Considerations

### Pipeline privilege separation

Use genuinely distinct identities for plan and apply, not just distinct
pipeline stages sharing the same underlying credential — the security
value of separating plan from apply is largely lost if a compromised
plan-stage credential can also apply, since plan-stage code (evaluated on
every pull request, including from less-trusted contributors in an
open-source or large-organization context) is inherently more exposed
than the gated apply stage.

### Drift detection frequency and scope

Balance drift-detection frequency against cost and noise: too infrequent,
and drift accumulates unnoticed for an extended window; too frequent, and
the scheduled plan runs themselves become a meaningful cost and a source
of alert fatigue if every run produces a notification regardless of
whether drift was actually found. Alert only on detected drift, not on
every completed scheduled run, and tune frequency to the environment's
actual rate of legitimate out-of-band change (production environments
with strict change control can run less frequent checks than
fast-moving development environments).

### Observability data retention and cost

High-cardinality metrics, full structured logs, and complete traces are
each individually expensive to retain at full fidelity indefinitely.
Design retention tiers deliberately: full-fidelity, high-cost retention
for a shorter recent window (adequate for active incident investigation),
with progressively down-sampled or summarized retention for
longer-term trend analysis — applying the same storage-tiering
cost-versus-access-latency trade-off from [Chapter 06](06-cloud-storage-databases-and-data-services.md) to observability
data specifically.

### Scoping chaos experiments safely

Run chaos experiments first in non-production, then in production with a
narrow, reversible blast radius (a single instance, a single non-critical
service, during a low-traffic window with an engineer actively
monitoring), before ever running an experiment against a component with a
genuinely uncontrolled blast radius. The goal is validating a specific
resilience hypothesis with an acceptable, bounded risk — not creating an
actual incident in the course of testing for one; treat "we caused an
unintended outage while chaos testing" as a process failure requiring the
experiment's blast-radius controls to be revisited, not an acceptable cost
of the practice.

### Lifecycle ownership at scale

As the resource count grows, manual ownership tracking degrades quickly.
Prefer deriving ownership and lifecycle state from enforced tags and
account/subscription structure ([Chapter 08](08-cloud-governance-security-and-finops.md)) queried programmatically over
maintaining a separate, manually updated spreadsheet or wiki page of
resource ownership, which reliably goes stale. Automate the notification
and eventual decommissioning of resources whose expiration tag has
passed, with a grace period and notification to the tagged owner before
actual deletion.

## Implementation and Automation

### CI/CD pipeline with plan/apply separation

```yaml
# .ci/infrastructure-pipeline.yml — illustrative plan/apply separation.
stages:
  - plan
  - apply

plan:
  stage: plan
  # Uses a read-only, federated identity (Chapter 03 pattern).
  script:
    - terraform init
    - terraform plan -out=tfplan
    - terraform show -json tfplan > tfplan.json
    - conftest test tfplan.json --policy policy # Chapter 02/08 guardrails
  artifacts:
    paths: [tfplan]
  rules:
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'

apply:
  stage: apply
  # Uses a distinct, more privileged federated identity than plan.
  script:
    - terraform apply tfplan
  dependencies: [plan]
  environment: production
  when: manual # requires explicit human approval after plan review
  rules:
    - if: '$CI_COMMIT_BRANCH == "main"'
```

### Scheduled drift detection

```yaml
# .ci/drift-detection.yml — illustrative scheduled, read-only drift check.
drift_check:
  script:
    - terraform init
    - terraform plan -detailed-exitcode -out=drift.plan
    # Exit code 2 means drift detected (a diff exists); 0 means no drift;
    # 1 means an actual error. Alert only on 2, not on every run.
  after_script:
    - |
      if [ "$CI_JOB_STATUS" == "failed" ] && [ "$EXIT_CODE" == "2" ]; then
        ./scripts/notify-drift-detected.sh --environment "$CI_ENVIRONMENT_NAME"
      fi
  schedule: "0 */6 * * *" # every 6 hours; tune to environment change rate
```

### Structured logging with a correlated trace identifier

```json
{
  "timestamp": "2026-07-18T14:32:01Z",
  "level": "error",
  "trace_id": "4bf92f3577b34da6a3ce929d0e0e4736",
  "service": "checkout-api",
  "message": "downstream payment service call failed",
  "downstream_service": "payment-processor",
  "http_status": 503,
  "latency_ms": 4210
}
```

```hcl
# observability.tf — illustrative alerting metric tied to the same
# service/trace correlation used in structured logs above.
resource "cloud_metric_alarm" "checkout_error_rate" {
  name        = "checkout-api-error-rate-high"
  metric      = "checkout-api.error_rate"
  threshold    = 0.01 # 1%
  evaluation_periods = 3
  period_seconds   = 60

  notification_targets = [cloud_notification_channel.platform_oncall.id]
}
```

### Chaos experiment as code

```yaml
# chaos/zone-failure-experiment.yml — illustrative chaos experiment
# definition, run against a non-critical service first.
title: "Zone B failure — checkout-api"
hypothesis: >
  If zone B becomes unavailable, checkout-api traffic shifts to zones A
  and C within 60 seconds with no sustained error-rate increase above
  baseline.
method:
  - action: cordon_zone
    target: checkout-api-autoscaling-group
    zone: b
    duration_seconds: 300
rollback:
  - action: uncordon_zone
    target: checkout-api-autoscaling-group
    zone: b
success_criteria:
  - metric: checkout-api.error_rate
    condition: "stays below baseline + 0.5% throughout the experiment"
  - metric: checkout-api.zone_b_traffic_share
    condition: "drops to 0% within 60 seconds of experiment start"
```

### Automated lifecycle expiration

```hcl
# lifecycle-policy.tf — illustrative expiration-tag enforcement.
resource "cloud_policy" "enforce_expiration_tag" {
  name  = "temporary-resource-expiration"
  scope  = var.sandbox_account_id
  effect = "deny"

  condition {
    missing_tag                = "expires_on"
    applies_to_resource_types  = ["compute_instance", "managed_database"]
  }

  enforcement_mode = "deny" # sandbox is a safe scope for enforcing mode directly
}
```

## Validation and Troubleshooting

- **Diagnose a failed apply by reading the plan it was approved against,
  not just the error message** — a common cause of apply-time failure is
  a state change between plan and apply (someone else's change landed
  first); re-run plan before retrying apply rather than blindly retrying
  the stale plan.
- **Diagnose repeated drift on the same resource as a process gap, not
  only a technical one** — trace who or what made the out-of-band
  change (cloud provider audit logs are the authoritative source) and
  address why the pipeline was bypassed, in addition to reconciling the
  drift itself.
- **Distinguish a monitoring gap from an observability gap during an
  incident retrospective.** If the team knew something was wrong quickly
  but could not determine why, that is an observability gap (better
  traces or structured logs needed); if the team did not know something
  was wrong until a customer reported it, that is a monitoring gap
  (missing alert or threshold).
- **Validate chaos experiment rollback before running the experiment
  itself** — confirm the rollback action (like `uncordon_zone` above)
  works correctly in isolation first, so a failed experiment cannot leave
  the system in the degraded state longer than intended.
- **Reconcile inventory drift for unmanaged resources by importing, not
  deleting, on first discovery** — a resource discovered outside of code
  may still be actively serving production traffic; confirm purpose and
  ownership before any decommissioning action, and only delete after that
  confirmation fails to find an owner within a defined grace period.

## Security and Best Practices

- Enforce plan/apply identity separation and require human approval on
  apply for any environment above sandbox, consistent with the
  just-in-time elevation guidance from [Chapter 03](03-cloud-identity-access-and-cryptographic-services.md).
- Run policy-as-code guardrail evaluation (Chapters 02 and 08) as a
  required, blocking step in the plan stage — a plan that violates a
  guardrail should never reach the apply stage for approval in the first
  place.
- Treat drift-detection findings as a security signal, not only an
  operational one — an out-of-band change is also a plausible indicator
  of unauthorized access, and should be reviewed with that possibility in
  mind, not assumed benign by default.
- Redact or tokenize sensitive fields (credentials, personal data) before
  they reach structured logs or traces; observability infrastructure
  itself becomes a sensitive data store the moment it captures request
  payloads containing sensitive fields.
- Scope chaos experiment tooling's own permissions narrowly and audit its
  use — a tool capable of deliberately degrading production
  infrastructure is a high-value target and should be governed with the
  same rigor as any other high-privilege automation.
- Automate decommissioning notification and grace periods rather than
  immediate deletion, but do not let "grace period" become indefinite
  retention in practice — track and alert on expiration-tagged resources
  that have exceeded their grace period without resolution.

## References and Knowledge Checks

### References

- Beyer, B., Jones, C., Petoff, J., Murphy, N., *Site Reliability
  Engineering* (O'Reilly), for observability and error-budget practice
  informing this chapter's monitoring/observability distinction.
- Principles of Chaos Engineering (principlesofchaos.org).
- OpenTelemetry documentation, for the current vendor-neutral standard
  covering metrics, logs, and traces instrumentation.
- `SOFTWARE_VERSIONS.md` in this repository for the Terraform baseline.

### Knowledge checks

1. Why does separating plan and apply into distinct pipeline stages with
   distinct identities provide more security value than separating them
   into stages that share one credential?
2. A team detects the same resource drifting out of code-defined state
   every week. What two things should be investigated, beyond simply
   reconciling the drift again?
3. Explain the practical difference between a monitoring gap and an
   observability gap using an incident retrospective as the diagnostic
   lens.
4. Why should a chaos experiment's rollback action be validated in
   isolation before the experiment itself is run?
5. A resource is discovered outside of infrastructure-as-code with no
   identifiable owner. What is the correct first action, and why is
   immediate deletion the wrong first action?

## Hands-On Lab

### Lab 9.1 — Drift detection and remediation pipeline

This lab simulates the full drift-detection cycle locally: a Terraform-
managed local resource is modified out-of-band (simulating a manual
console change), detected by a scheduled plan check, and reconciled. It
uses only the local `local_file` provider, so no cloud account or
credentials are required.

**Prerequisites**

- Terraform 1.9.x or later, or a compatible OpenTofu release.
- A POSIX shell and `jq`.

**Steps**

1. Create the working directory:

   ```bash
   mkdir -p ~/labs/vol07-ch09 && cd ~/labs/vol07-ch09
   ```

2. Create `main.tf`, a simulated managed resource:

   ```hcl
   terraform {
     required_providers {
       local = { source = "hashicorp/local", version = ">= 2.5" }
     }
   }

   resource "local_file" "managed_config" {
     filename = "${path.module}/managed-config.json"
     content = jsonencode({
       environment = "prod"
       replicas    = 3
       managed_by  = "terraform"
     })
   }
   ```

3. Initialize and apply to establish the baseline managed state:

   ```bash
   terraform init
   terraform apply -auto-approve
   ```

   **Expected result:** `Apply complete! Resources: 1 added.` and
   `managed-config.json` exists with `"replicas": 3`.

4. Run a drift check using `-detailed-exitcode`, confirming no drift
   exists yet:

   ```bash
   terraform plan -detailed-exitcode -out=drift.plan; echo "exit code: $?"
   ```

   **Expected result:** `exit code: 0`, meaning no differences —
   confirming the deployed state currently matches code.

5. Simulate an out-of-band change (someone edited the "resource" directly
   outside the pipeline, bypassing plan/apply entirely):

   ```bash
   jq '.replicas = 5' managed-config.json > tmp.json && mv tmp.json managed-config.json
   cat managed-config.json
   ```

   **Expected result:** The file now shows `"replicas": 5`, simulating
   drift between code-defined intent (3) and actual deployed state (5).

6. Run the drift check again:

   ```bash
   terraform plan -detailed-exitcode -out=drift.plan; echo "exit code: $?"
   ```

   **Expected result:** `exit code: 2`, indicating drift was detected
   (Terraform's plan shows it intends to restore `content` to the
   code-defined value). This is the signal a scheduled drift-detection
   job in a real pipeline would alert on.

7. Reconcile the drift by applying the saved plan, restoring the
   code-defined state:

   ```bash
   terraform apply drift.plan
   cat managed-config.json
   ```

   **Expected result:** `managed-config.json` shows `"replicas": 3`
   again, and a subsequent `terraform plan -detailed-exitcode` (run it to
   confirm) returns exit code `0`.

**Negative test**

8. Confirm the drift check correctly reports no drift (exit code `0`,
   not a false positive) immediately after a normal, in-pipeline change.
   Edit `main.tf` to change `replicas` to `4` (a legitimate, code-reviewed
   change this time, not an out-of-band edit), then:

   ```bash
   terraform apply -auto-approve
   terraform plan -detailed-exitcode; echo "exit code: $?"
   ```

   **Expected result:** `exit code: 0` — confirming the drift check does
   not false-positive against a change made correctly through code and
   apply, only against out-of-band divergence from code.

**Cleanup**

9. Destroy and remove the working directory:

   ```bash
   terraform destroy -auto-approve
   cd ~ && rm -rf ~/labs/vol07-ch09
   ```

   **Expected result:** Terraform reports the resource destroyed, and the
   working directory no longer exists.

## Summary and Completion Checklist

This chapter closes the volume with the operational practices that keep a
cloud environment trustworthy over time: plan/apply pipeline separation
with distinct identities, continuous drift detection and deliberate
reconciliation, the distinction between monitoring (known questions) and
observability (unanticipated questions) across metrics, logs, and traces,
chaos engineering as the discipline that validates resilience assumptions
before a real failure does, and a resource lifecycle practice that
prevents orphaned and unmanaged resources from accumulating silently.
Together with Chapters 01 through 08, this completes Volume VII's
provider-neutral treatment of cloud infrastructure architecture, identity,
networking, compute, data, hybrid/multicloud design, and governance —
[Volume XVII](../../volume-17-aws-architecture-security/README.md) applies these concepts to AWS's specific console, CLI, and
service implementation in depth.

- [ ] Can explain why plan and apply should use distinct identities, not
      just distinct pipeline stages.
- [ ] Can design a drift-detection schedule and reconciliation process
      for a managed environment.
- [ ] Can distinguish a monitoring gap from an observability gap using an
      incident retrospective.
- [ ] Can design a bounded, safe chaos experiment with a stated hypothesis
      and validated rollback.
- [ ] Completed Lab 9.1, including the negative test and cleanup.
