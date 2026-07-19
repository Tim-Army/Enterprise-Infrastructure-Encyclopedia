# Chapter 04: Enterprise Logging, Event Management, and Retention

![Lab flow for this chapter: a script writes structured JSON log lines, one carrying an authorization bearer token; Vector parses each line as JSON and removes the authorization field before shipping to Loki, and querying Loki confirms all entries arrived with the field absent even from the one that originally carried it. As a negative test, querying specifically for a non-empty authorization field returns zero results, confirming enforcement rather than mere display omission; commenting out the redaction transform, restarting Vector, and re-emitting logs causes the same query to return the previously redacted value in plain text.](../../../diagrams/volume-11-observability-enterprise-operations/chapter-04-vector-loki-pii-redaction-flow.svg)

*Figure 4-1. Flow used throughout this chapter's Hands-On Lab: a Vector-to-Loki log pipeline redacting a sensitive field before ingestion, tested with the redaction transform removed.*

## Learning Objectives

- Differentiate structured logs, unstructured logs, and discrete events,
  and explain when each is the appropriate signal to emit.
- Design a log pipeline (collection, processing, storage) that scales to
  enterprise volume without collection agents becoming a source of data
  loss or host resource contention.
- Write LogQL queries against a label-indexed log store and explain why
  its indexing model differs from full-text search.
- Correlate logs with traces and metrics using shared identifiers
  (`trace_id`, `service.name`) established in [Chapter 02](02-telemetry-architecture-instrumentation-and-pipelines.md).
- Apply a tiered retention policy that balances investigation needs,
  storage cost, and regulatory retention obligations.
- Diagnose common logging pipeline failures: agent backpressure, log
  loss during rotation, and unbounded label cardinality in a
  label-indexed store.

## Theory and Architecture

### Structured logs, unstructured logs, and events

A **log** is a timestamped record of something a system did or observed,
emitted from inside a running process at the point the event occurred.
**Unstructured logs** are free-text lines intended for human reading
(`ERROR: failed to connect to db, retrying...`); they are cheap to emit
and immediately readable but expensive to query reliably at scale,
because extracting a field requires parsing the string with a
regular expression that a later, subtly reformatted log line silently
breaks. **Structured logs** emit a defined schema, almost always JSON,
with consistent field names (`level`, `message`, `service.name`,
`trace_id`, plus event-specific fields):

```json
{"timestamp":"2026-07-18T14:32:07.114Z","level":"error","service.name":"checkout-api","trace_id":"5b8aa5a2d2c872e8321cf37308d69df2","message":"payment gateway timeout","gateway":"primary","attempt":2,"deployment.environment.name":"production"}
```

Structured logging is the enterprise default for anything beyond a
single developer's local debugging session: it is machine-parseable
without a fragile regular expression, it composes with the same
semantic-convention field names used in metrics and traces ([Chapter 02](02-telemetry-architecture-instrumentation-and-pipelines.md)),
and it lets a query engine filter and aggregate on fields directly rather
than on substrings.

An **event** is a discrete, structured record of something that
happened, is not necessarily emitted from inside a request's execution
path, and typically has a defined schema published and versioned
independently of any one service's logging output — a user account
created, a feature flag toggled, a configuration change applied. Events
often flow through a message bus (Kafka, an event-streaming platform)
rather than a logging pipeline, and they frequently have downstream
consumers beyond observability (analytics, billing, audit). The
practical operational distinction: logs are diagnostic exhaust a service
produces about its own execution; events are business-meaningful facts a
service publishes on purpose for other systems to consume. A
well-instrumented enterprise system treats these as related but separate
concerns — do not route billing-critical events only through a log
pipeline with a 30-day retention and no delivery guarantee.

### Log levels and their operational meaning

A conventional level hierarchy (`TRACE`, `DEBUG`, `INFO`, `WARN`,
`ERROR`, `FATAL`) exists to let both humans and automated tooling filter
volume without losing signal. The levels matter operationally, not just
stylistically:

- **DEBUG/TRACE** — high-volume, disabled by default in production, and
  enabled temporarily and scoped narrowly (a specific service instance,
  a specific request via a debug header) during active investigation,
  never left on fleet-wide.
- **INFO** — normal operational milestones (request completed, job
  started) — the highest-volume level typically shipped in production,
  and the first candidate for sampling or exclusion when a service's log
  volume exceeds its pipeline or cost budget.
- **WARN** — a condition that is recoverable but notable: a retry
  succeeded, a fallback path was used, a deprecated API was called.
- **ERROR** — an operation failed and the failure is visible to the
  caller or otherwise consequential; this is the level most incident
  investigations query first.
- **FATAL** — the process cannot continue and is terminating; rare, and
  every occurrence typically warrants automatic alerting.

Setting the wrong default level fleet-wide is a common and expensive
mistake in both directions: `DEBUG` in production floods the pipeline
and inflates cost; `ERROR`-only in production discards the `WARN`-level
context (a retry that succeeded twice before finally failing) that often
explains *why* a later error happened. `INFO` is the correct default for
most production services, with `DEBUG` available as a dynamically
toggled override (a feature flag or runtime configuration reload, not a
redeploy) scoped to the investigation at hand.

### The log pipeline: collection, processing, storage

Enterprise log pipelines separate three concerns, structurally similar to
the OTel Collector's agent/gateway split from [Chapter 02](02-telemetry-architecture-instrumentation-and-pipelines.md):

- **Collection** — an agent (Fluent Bit, Vector, or the OpenTelemetry
  Collector's `filelog` receiver) running on every host or as a
  Kubernetes DaemonSet, tailing log files or a container runtime's log
  stream, adding resource attributes (pod name, node, namespace), and
  forwarding onward. Collection agents must handle log rotation without
  data loss (tracking file inode, not just path, so a rotated file is
  drained rather than silently abandoned) and must apply backpressure
  correctly — a collection agent that blocks the application's write
  path when downstream is saturated can turn a logging pipeline outage
  into an application outage, the same failure mode [Chapter 02](02-telemetry-architecture-instrumentation-and-pipelines.md) covers
  for telemetry export generally.
- **Processing** — parsing (structured JSON parsed directly; legacy
  unstructured lines parsed with a defined grok-style pattern),
  enrichment (adding `trace_id` correlation where missing, adding
  ownership metadata from the service catalog), redaction (removing PII
  and secrets before the log leaves the trust boundary, per [Chapter 02](02-telemetry-architecture-instrumentation-and-pipelines.md)'s
  design principle), and routing (splitting streams by destination — a
  hot, queryable store for recent operational logs, a cold archive for
  compliance retention, and potentially a SIEM for security-relevant
  logs, covered further in [Volume X](../../volume-10-enterprise-cybersecurity/README.md)).
- **Storage** — a log backend optimized for the query pattern the
  organization actually uses. Two dominant models exist: full-text
  indexed search (Elasticsearch/OpenSearch) indexes every field and
  supports free-text search at high storage and indexing cost; label-
  indexed storage (Grafana Loki) indexes only a small set of labels
  (`service.name`, `deployment.environment.name`, `level`) and stores
  log content itself as compressed, unindexed chunks, trading full-text
  search performance for dramatically lower storage and operating cost
  at high volume. Enterprises frequently run both: label-indexed storage
  for general operational logging at volume, full-text search for
  security and compliance workloads that require broad ad hoc text
  search ([Volume X](../../volume-10-enterprise-cybersecurity/README.md) covers SIEM sizing in depth).

```text
[ app container stdout ] --tail--> [ node collection agent ] --process/redact/route--> [ hot store (queryable) ]
                                                                                   \--> [ cold archive (compliance) ]
                                                                                   \--> [ SIEM (security-relevant subset) ]
```

### LogQL and the label-indexed query model

LogQL (Loki's query language) mirrors PromQL's structure deliberately: a
log-stream selector filters by indexed labels, and a pipeline of
operators filters and extracts from the log content within the matched
streams:

```logql
# All error-level logs from checkout-api in production
{service_name="checkout-api", deployment_environment_name="production"} | json | level="error"

# Rate of error logs per second, over 5 minutes (log-derived metric)
sum(rate({service_name="checkout-api"} | json | level="error" [5m]))

# Extract a specific field and filter on its value
{service_name="checkout-api"} | json | gateway="primary" | attempt > 1
```

The critical architectural distinction from a full-text index: the
`{service_name="checkout-api", ...}` stream selector must match on
*indexed labels only*, and only a deliberately small set of labels is
indexed. Everything after the stream selector (`| json | level="error"`)
is evaluated by scanning the matched streams' log content at query time,
not via an index. This is why label-indexed storage is cheap to ingest
at volume (no per-field index to maintain) but requires disciplined label
design: too few labels and a query must scan more log volume than
necessary; too many labels, or a label with unbounded values (a request
ID, a user ID used as a label instead of a queryable field), and the
label index itself explodes in cardinality, degrading the store the same
way unbounded metric labels degrade Prometheus ([Chapter 02](02-telemetry-architecture-instrumentation-and-pipelines.md)). The rule of
thumb: labels are for the small set of dimensions you filter *by*
(service, environment, level, region); fields extracted with `| json`
are for everything you filter *on the value of* after narrowing the
stream.

### Correlating logs with traces and metrics

A log line's diagnostic value multiplies when it carries the same
`trace_id` a distributed trace uses ([Chapter 05](05-distributed-tracing-profiling-and-dependency-analysis.md)) — an engineer
investigating a slow trace span can pivot directly to the exact log
lines emitted during that span, and an engineer starting from an
alarming log line can pivot directly to the full trace for that request.
This requires the logging library to read the active trace context (the
OTel SDK exposes the current span's trace and span ID to the logging
layer) and inject it into every structured log line automatically,
rather than relying on developers to add it manually to each log call —
manual injection is inconsistently applied and the gaps are discovered
only during an incident, when it is too late to matter.

## Design Considerations

- **Sampling logs, not just traces.** At sufficient request volume,
  logging every `INFO`-level line for every request is not affordable.
  Apply head-based log sampling for high-volume, low-value log lines
  (successful health checks, routine `INFO` milestones) while
  guaranteeing 100% capture for `ERROR`/`WARN` and for any log line
  belonging to a trace that was itself sampled for retention ([Chapter 05](05-distributed-tracing-profiling-and-dependency-analysis.md))
  — correlating a kept trace with a discarded log defeats the
  correlation benefit above.
- **Retention tiering.** Not all logs warrant the same retention. A
  common enterprise tiering: hot/queryable retention of 14-30 days for
  general operational logs (matched to typical incident investigation
  windows), a compressed cold archive of 1-7 years for logs with a
  regulatory retention obligation (audit logs, authentication events,
  financial transaction logs — [Volume X](../../volume-10-enterprise-cybersecurity/README.md) and applicable regulatory
  frameworks such as PCI DSS or SOX drive the exact figure), and
  immediate, permanent exclusion at the source for anything that should
  never be logged at all (raw payment card numbers, plaintext
  passwords).
- **Cost model and volume budget.** Log volume, unlike metrics volume,
  scales roughly linearly with request volume and log-line verbosity
  simultaneously, making it the single largest observability cost line
  item at enterprise scale in most organizations. Assign each service
  team an explicit log-volume budget (bytes/day or a cost figure) visible
  on a shared dashboard, the same way a cloud cost budget is tracked,
  rather than leaving volume growth to be discovered only when a
  platform-wide bill spikes.
- **Full-text search versus label-indexed storage, by workload.**
  Choose based on actual query pattern, not habit: an operations team
  that mostly filters by service/environment/level and reads surrounding
  context is well served by label-indexed storage at much lower cost; a
  security team that must search arbitrary free text across the entire
  fleet for an indicator of compromise needs full-text indexing capacity
  for that specific workload. Running both is common; running only
  full-text at full operational log volume is the most frequent
  unnecessary-cost pattern encountered in practice.
- **PII and regulatory scope creep.** A log line that seemed
  harmless when written (`user.email` for debugging convenience) can
  bring an entire log store into scope for data-subject-access-request
  obligations or a compliance audit. Treat log field allow-listing, not
  block-listing, as the safer default for any field that might contain
  personal data — engineers reliably forget to add a new sensitive field
  to a block-list when they introduce it.
- **Multi-line log handling.** Stack traces and other multi-line
  unstructured output break naive line-based collection, fragmenting one
  logical event into many. Configure the collection agent's multi-line
  detection (a start-of-record regex, or better, emit structured JSON
  with the entire stack trace as one field value) explicitly rather than
  discovering the fragmentation during an incident review.

## Implementation and Automation

The following Vector configuration implements collection, JSON parsing,
PII redaction, and dual-destination routing (a hot Loki store and a cold
archive), illustrating the pipeline concerns above in a single
declarative file:

```toml
# vector.toml
[sources.container_logs]
type = "kubernetes_logs"

[transforms.parse_json]
type = "remap"
inputs = ["container_logs"]
source = '''
  . = parse_json!(.message)
  .k8s_pod_name = get_env_var!("HOSTNAME")
'''

[transforms.redact_pii]
type = "remap"
inputs = ["parse_json"]
source = '''
  if exists(.user_email) { .user_email = redact(.user_email, filters: ["email"]) }
  if exists(.authorization) { del(.authorization) }
  if exists(.credit_card) { del(.credit_card) }
'''

[transforms.route_by_level]
type = "route"
inputs = ["redact_pii"]
[transforms.route_by_level.route]
errors_and_warnings = '.level == "error" || .level == "warn"'

[sinks.loki_hot]
type = "loki"
inputs = ["redact_pii"]
endpoint = "http://loki-gateway.observability.svc:3100"
encoding.codec = "json"
[sinks.loki_hot.labels]
service_name = "{{ service.name }}"
deployment_environment_name = "{{ deployment.environment.name }}"
level = "{{ level }}"

[sinks.cold_archive]
type = "aws_s3"
inputs = ["route_by_level.errors_and_warnings"]
bucket = "enterprise-log-archive-prod"
key_prefix = "date=%Y-%m-%d/service={{ service.name }}/"
compression = "gzip"
encoding.codec = "json"
```

This topology sends the full redacted stream to the hot, queryable Loki
store with a short retention (configured at the store, not here), while
routing only `error`/`warn`-level lines to a compressed, long-retention
S3 archive — matching the cost-tiering design principle above by not
archiving high-volume, low-value `INFO` traffic.

Enforce log-field redaction rules as policy-as-code, tested independently
of the pipeline, so a new sensitive field is caught before it reaches
production:

```python
# test_redaction_policy.py — run in CI against sample log payloads
import json
import subprocess

SENSITIVE_FIELDS = ["authorization", "credit_card", "ssn", "password"]

def test_no_sensitive_fields_in_output():
    sample = json.dumps({
        "level": "info",
        "message": "charge processed",
        "authorization": "Bearer secret-token",
        "credit_card": "4111111111111111",
    })
    result = subprocess.run(
        ["vector", "test", "--config", "vector.toml"],
        input=sample, capture_output=True, text=True,
    )
    output = json.loads(result.stdout)
    for field in SENSITIVE_FIELDS:
        assert field not in output, f"{field} leaked through redaction pipeline"
```

Set retention per label-selected stream at the Loki store using its
compactor configuration, implementing the tiered retention design
directly:

```yaml
# loki-config.yaml (excerpt)
limits_config:
  retention_period: 720h  # 30-day default
compactor:
  retention_enabled: true
  retention_delete_delay: 2h
overrides:
  # Audit-relevant streams get a longer retention override.
  tenant-audit:
    retention_period: 61320h  # ~7 years
```

## Validation and Troubleshooting

- **Confirm no data loss across log rotation.** Rotate a log file
  manually (`logrotate -f` against the target config, or `mv` plus
  signal the writer to reopen) while tailing volume with the collection
  agent, and confirm the line count collected matches the line count
  written, using a known-count synthetic burst before and after the
  rotation event.
- **Symptom: log volume from a single service spikes unexpectedly.**
  Query the label-indexed store's per-stream byte rate
  (`sum(rate({service_name="checkout-api"}[5m])) by (service_name)` in
  LogQL, or the equivalent ingestion-rate metric the store exposes) and
  correlate the spike time with the service's deploy history — a common
  root cause is a `DEBUG`-level flag left enabled after a debugging
  session, or a new error path that logs a full stack trace per request
  in a retry loop.
- **Symptom: correlated trace exists but no log lines are found by
  `trace_id`.** Confirm the logging library is actually reading the
  active span context at the point of the log call (not, for example, in
  code that logs from a background thread or an async callback that lost
  the OTel context), which is the most common cause of correlation gaps
  and is often intermittent, appearing only for asynchronous code paths.
- **Symptom: label cardinality alert on the log store.** Identify the
  offending label (not field) using the store's own cardinality-
  reporting endpoint, and confirm whether a recent pipeline configuration
  change (Vector `labels` block above) started templating an unbounded
  value — a request ID or user ID — directly into a label instead of
  leaving it as an extractable JSON field.
- **Silent redaction failure.** Periodically send a known-sensitive
  synthetic payload through the full pipeline (the CI test above, run
  against the live pipeline on a schedule, not only pre-deploy) and
  confirm it does not appear unredacted in the hot store — redaction
  logic silently failing after an unrelated pipeline refactor is a
  realistic and serious data-exposure risk that a one-time test at
  initial rollout does not catch.

## Security and Best Practices

- Redact or exclude sensitive fields at the earliest pipeline stage
  (ideally the application's structured-logging library itself, before
  the line is even written to stdout), not only at the central
  collection agent — logs written to local disk before redaction are
  already at risk if the host is compromised or if local log files are
  collected by an unrelated tool.
- Apply the same allow-list-over-block-list principle from [Chapter 02](02-telemetry-architecture-instrumentation-and-pipelines.md) to
  log field emission: define which fields a structured log event may
  contain by schema, rather than trying to enumerate every field that
  must never appear.
- Encrypt log data in transit (TLS from collection agent to storage) and
  at rest (both hot store and cold archive), and scope access to the log
  store with the same least-privilege principle as the service catalog
  in [Chapter 01](01-observability-operating-model-and-service-ownership.md) — read access to another team's operational logs during
  cross-service debugging is often appropriate, but bulk export access
  should be restricted and logged.
- Treat audit-relevant logs (authentication, authorization changes,
  administrative actions) as a distinct, integrity-protected stream:
  route them to storage with write-once retention (object lock or
  equivalent) so their own audit trail cannot be altered or truncated by
  someone attempting to cover an action, including a compromised
  administrative account.
- Log access to the log store itself. Who queried what, and when, is
  part of the audit trail for a regulated environment, and its absence
  is a common finding in security assessments of otherwise
  well-instrumented platforms.
- Coordinate log retention policy with legal and compliance
  stakeholders, not only platform engineering — retention that is too
  short can violate a regulatory minimum, and retention that is too long
  can violate a data-minimization obligation or a "right to be
  forgotten" requirement under applicable privacy law.

## References and Knowledge Checks

**References**

- [Grafana Loki documentation, `grafana.com/docs/loki/latest/`, for the
  label-indexed storage model and LogQL.](https://grafana.com/docs/loki/latest/)
- [Vector documentation, `vector.dev/docs/`, for pipeline transform (VRL)
  syntax and sink configuration.](https://vector.dev/docs/)
- [OpenTelemetry Logs specification, `opentelemetry.io/docs/specs/otel/logs/`,
  for structured log data model and trace-context correlation.](https://opentelemetry.io/docs/specs/otel/logs/)
- NIST SP 800-92, *Guide to Computer Security Log Management*, for
  general log management and retention guidance referenced further in
  [Volume X](../../volume-10-enterprise-cybersecurity/README.md).

**Knowledge Checks**

1. Explain the practical difference between a log and an event, and give
   an example of data that should be published as an event rather than
   only logged.
2. Why does a label-indexed log store require disciplined label design,
   and what happens if an unbounded value is used as a label instead of
   an extracted field?
3. Describe two failure modes that result from setting a fleet-wide
   default log level of `DEBUG` versus `ERROR`-only.
4. What causes a `trace_id`-based log correlation gap even when both the
   tracing and logging pipelines are individually healthy?
5. Why should PII redaction happen at the application's logging library
   rather than only at the central collection agent?

## Hands-On Lab

**Objective:** Deploy a local log pipeline (Vector plus Loki), ship
structured JSON logs from a sample application, run LogQL queries by
label and by extracted field, and validate a PII redaction rule with a
positive and negative test.

### Prerequisites

- Docker Engine and Docker Compose v2.
- `curl` and a POSIX shell.
- Approximately 1.5 GB of free memory for the lab stack.

### Procedure

1. Create the lab directory and a script that emits structured JSON log
   lines to a file, simulating an application's log output, including
   one line with a sensitive field to validate redaction:

   ```bash
   mkdir -p ~/log-lab/logs && cd ~/log-lab
   cat > emit-logs.sh <<'EOF'
   #!/usr/bin/env bash
   set -euo pipefail
   for i in $(seq 1 20); do
     echo "{\"timestamp\":\"$(date -u +%Y-%m-%dT%H:%M:%S.%3NZ)\",\"level\":\"info\",\"service_name\":\"lab-app\",\"deployment_environment_name\":\"production\",\"message\":\"request completed\",\"attempt\":1}" >> logs/lab-app.log
     sleep 0.2
   done
   echo "{\"timestamp\":\"$(date -u +%Y-%m-%dT%H:%M:%S.%3NZ)\",\"level\":\"error\",\"service_name\":\"lab-app\",\"deployment_environment_name\":\"production\",\"message\":\"payment gateway timeout\",\"authorization\":\"Bearer super-secret-token\",\"attempt\":2}" >> logs/lab-app.log
   EOF
   chmod +x emit-logs.sh
   ```

2. Create a Vector configuration that reads the log file, parses JSON,
   redacts the `authorization` field, and ships to Loki:

   ```bash
   cat > vector.toml <<'EOF'
   [sources.file_logs]
   type = "file"
   include = ["/logs/lab-app.log"]

   [transforms.parse_json]
   type = "remap"
   inputs = ["file_logs"]
   source = '''
     . = parse_json!(.message)
   '''

   [transforms.redact]
   type = "remap"
   inputs = ["parse_json"]
   source = '''
     if exists(.authorization) { del(.authorization) }
   '''

   [sinks.loki_out]
   type = "loki"
   inputs = ["redact"]
   endpoint = "http://loki:3100"
   encoding.codec = "json"
   labels.service_name = "{{ service_name }}"
   labels.deployment_environment_name = "{{ deployment_environment_name }}"
   labels.level = "{{ level }}"
   EOF
   ```

3. Create the Compose file for Loki and Vector, and start Loki first:

   ```bash
   cat > docker-compose.yaml <<'EOF'
   services:
     loki:
       image: grafana/loki:3.2.1
       ports:
         - "3100:3100"
     vector:
       image: timberio/vector:0.43.0-debian
       volumes:
         - ./vector.toml:/etc/vector/vector.toml:ro
         - ./logs:/logs:ro
       command: ["--config", "/etc/vector/vector.toml"]
       depends_on:
         - loki
   EOF
   docker compose up -d loki
   sleep 5
   docker compose up -d vector
   ```

4. Run the log emitter to generate sample traffic, including the
   sensitive-field line:

   ```bash
   ./emit-logs.sh
   sleep 5
   ```

5. Query Loki directly via its HTTP API (equivalent to a LogQL query run
   from Grafana's Explore view) to confirm ingestion and redaction:

   ```bash
   curl -s -G "http://localhost:3100/loki/api/v1/query_range" \
     --data-urlencode 'query={service_name="lab-app"}' \
     --data-urlencode 'limit=50' | python3 -m json.tool
   ```

### Expected Results

The query returns 21 log entries for stream `{service_name="lab-app"}`.
Twenty entries have `level="info"` with `message="request completed"`.
One entry has `level="error"` with
`message="payment gateway timeout"`. Confirm the `authorization` field
is absent from every returned entry, including the error entry that
originally carried it, proving the redaction transform ran before the
Loki sink.

### Negative Test

Query specifically for the field that should have been redacted, and
confirm it returns no matches, demonstrating the redaction is enforced
rather than merely omitted from a display:

```bash
curl -s -G "http://localhost:3100/loki/api/v1/query_range" \
  --data-urlencode 'query={service_name="lab-app"} | json | authorization != ""' \
  --data-urlencode 'limit=50' | python3 -m json.tool
```

Confirm the `result` array is empty. Then temporarily comment out the
`del(.authorization)` line in `vector.toml`, restart Vector
(`docker compose restart vector`), re-run `emit-logs.sh`, and confirm the
same query now returns the previously-redacted line with the
`authorization` value present — demonstrating the negative case: the
pipeline does not protect sensitive fields on its own, the transform
does, and removing the transform reintroduces the exposure.

### Cleanup

```bash
cd ~/log-lab
docker compose down -v
cd ~
rm -rf ~/log-lab
```

## Summary and Completion Checklist

Structured logging, disciplined log levels, and a collection-processing-
storage pipeline with tiered retention turn diagnostic exhaust into a
queryable, cost-controlled asset rather than an unbounded liability.
Label-indexed storage trades full-text search for cost efficiency at
volume and requires the same cardinality discipline metrics do.
`trace_id` correlation is what lets an engineer move fluidly between
metrics, traces, and logs during an investigation — the connective
tissue this chapter and [Chapter 02](02-telemetry-architecture-instrumentation-and-pipelines.md) both depend on. [Chapter 05](05-distributed-tracing-profiling-and-dependency-analysis.md) continues
with distributed tracing itself; [Chapter 06](06-actionable-alerting-on-call-and-operations-centers.md) builds alerting on top of
log- and metric-derived signals together.

**Completion checklist**

- [ ] Can distinguish logs, structured logs, and events, and choose the
      right one for a given signal.
- [ ] Can write a LogQL query combining a label-based stream selector
      with a field-extraction filter.
- [ ] Can design a tiered retention policy balancing investigation
      needs, cost, and regulatory obligation.
- [ ] Deployed a working local log pipeline with JSON parsing, PII
      redaction, and label-based routing.
- [ ] Validated redaction with both a positive test (field absent) and a
      negative test (field present when the control is removed).
