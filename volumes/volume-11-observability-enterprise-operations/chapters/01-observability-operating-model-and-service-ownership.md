# Chapter 01: Observability Operating Model and Service Ownership

## Learning Objectives

- Distinguish monitoring from observability and explain why high-cardinality,
  high-dimensionality telemetry changes how enterprises investigate unknown
  failure modes.
- Describe the organizational operating models used to run observability at
  enterprise scale: centralized platform team, federated embedded ownership,
  and the hybrid "paved road" model.
- Apply service ownership principles (`you build it, you run it`) to define
  who is accountable for the health of a given service in a service catalog.
- Map an organization to Team Topologies interaction modes and identify
  where a dedicated observability or platform engineering team belongs.
- Design service-ownership metadata (catalog entries, escalation paths,
  tiering) that a paved-road observability platform can consume
  automatically.
- Evaluate an organization's observability maturity against a defined model
  and identify the next concrete investment.

## Theory and Architecture

### Monitoring versus observability

Monitoring answers questions you already thought to ask: is CPU above 80
percent, is the disk full, is the health-check endpoint returning `200`.
Monitoring is built around a finite, pre-declared set of checks and
dashboards. It works well for known failure modes in systems whose behavior
is well understood and slowly changing.

Observability is the property of a system that lets an operator ask
questions they did not anticipate at design time, using the telemetry the
system already emits, without shipping new code. The formal control-theory
definition — a system is observable if its internal state can be inferred
from its external outputs — maps directly onto distributed systems: if an
engineer can reconstruct what a request did, in which service, under which
conditions, from logs, metrics, and traces alone, the system is observable.

Modern distributed systems (microservices, serverless, service meshes,
Kubernetes-scheduled workloads with dynamic identity) have effectively
unbounded cardinality in their failure space: any combination of region,
version, tenant, feature flag, dependency latency, and node placement can
produce a unique failure signature. Pre-declared dashboards cannot
anticipate every combination. High-cardinality, high-dimensionality
telemetry — paired with tooling that lets an engineer slice by any
dimension ad hoc — is what makes novel failure modes tractable.

Observability does not replace monitoring; monitoring (threshold-based
alerting on known signals) remains the fastest way to detect that something
is wrong. Observability is how the organization determines *why* once
monitoring has raised the alarm. [Chapter 02](02-telemetry-architecture-instrumentation-and-pipelines.md) covers the telemetry pipeline
that produces this data; [Chapter 03](03-metrics-service-level-objectives-and-error-budgets.md) covers metrics and SLOs; [Chapter 05](05-distributed-tracing-profiling-and-dependency-analysis.md)
covers tracing. This chapter covers the organizational model that decides
who owns the result.

### The three pillars, and why "pillars" undersells it

Metrics, logs, and traces are commonly called the three pillars of
observability, with events and continuous profiles increasingly treated as
a fourth and fifth signal type (collectively sometimes abbreviated MELT:
Metrics, Events, Logs, Traces). Treating them as independent pillars is a
useful simplification for tooling but a poor mental model for
investigation: the value is in correlation. A metric spike identifies
*that* latency increased for a service; a trace identifies *which* request
path and downstream dependency contributed the latency; a log line
identifies *why* that specific call failed; a profile identifies *where* in
the code the CPU or memory went. An operating model that funds these
signals in separate tools, owned by separate teams, with no shared
identifiers (trace ID, service name, deployment version) between them
recreates the pre-observability world with more expensive tooling.

### Operating models

Enterprises converge on one of three operating models for observability,
usually evolving from the first to the third as scale increases:

1. **Centralized operations team.** A single NOC/SRE team owns all
   dashboards, alerts, and the on-call rotation for every service. This
   scales poorly past a few dozen services: the central team lacks context
   to interpret unfamiliar failure modes and becomes a bottleneck for
   onboarding new services.
2. **Fully federated (embedded) ownership.** Each product team owns its own
   instrumentation, dashboards, alerting, and on-call, with no shared
   platform. This scales engineering autonomy but produces tool sprawl,
   inconsistent SLO definitions, duplicated pipeline cost, and no
   cross-service correlation during a multi-service incident.
3. **Platform team plus paved road (hybrid).** A central observability
   platform team owns the telemetry pipeline, storage, tenancy, cost
   governance, and a small set of supported instrumentation libraries and
   dashboard/alert templates (the "paved road"). Product teams remain
   accountable for their own service's health and on-call, but they consume
   the platform rather than each building one. This is the model
   recommended for organizations beyond roughly 15-20 services, and it is
   the model assumed for the rest of this volume.

The hybrid model maps cleanly onto Team Topologies vocabulary: the
observability function is a **platform team** whose "thinnest viable
platform" is the telemetry pipeline and query layer; product engineering
teams are **stream-aligned teams** that consume it via a well-documented,
self-service **X-as-a-Service** interaction; a smaller **enabling team**
(often the same platform team, in a different mode) runs office hours and
onboarding support rather than long-lived collaboration. Avoid the
anti-pattern of the platform team becoming a **complicated-subsystem team**
that must be looped into every dashboard change — that recreates the
centralized bottleneck.

### Service ownership

"You build it, you run it" (attributed to Amazon's approach to service
teams) means the team that writes a service's code also carries its
production pager. This aligns incentives: teams that feel operational pain
from a design decision fix the design instead of filing a ticket against a
separate operations team. It requires three things to work at enterprise
scale:

- A **service catalog** that is the single source of truth for which team
  owns which service, its tier, its dependencies, and its escalation path.
- A **paved road** so that owning a service does not require every team to
  independently solve instrumentation, dashboards, and alert routing.
- An **error budget and SLO framework** ([Chapter 03](03-metrics-service-level-objectives-and-error-budgets.md)) so "run it" has an
  objective definition of "healthy" rather than being whatever the loudest
  stakeholder currently wants.

### Service tiering

Not every service warrants the same operational rigor. A common enterprise
tiering scheme:

| Tier | Definition | Example | On-call expectation |
| --- | --- | --- | --- |
| Tier 0 | Directly causes revenue loss or safety impact if down | Payment authorization, auth | 24/7 paged, &lt;5 min ack |
| Tier 1 | Degrades a primary product surface | Search, checkout UI | 24/7 paged, &lt;15 min ack |
| Tier 2 | Internal-facing or has a manual workaround | Internal reporting API | Business-hours paged |
| Tier 3 | Best-effort, no paging | Batch analytics job | Ticket-based, next business day |

Tier assignment drives SLO strictness, alert routing, change-freeze policy,
and which incidents trigger a formal major-incident process ([Chapter 07](07-service-management-incident-problem-and-change-operations.md)).

## Design Considerations

- **Where the platform team sits.** Reporting under a CTO/engineering
  organization keeps the platform team close to product needs; reporting
  under an infrastructure/IT organization keeps it close to network and
  compute telemetry. Either works; what matters is a funded mandate and a
  named executive sponsor, because the platform team's output (pipelines,
  templates, tenancy controls) is infrastructure that no single product
  team will fund on its own.
- **Buy versus build for the platform layer.** Enterprises rarely build a
  metrics or tracing backend from scratch today; the build decision is
  usually about the collection and pipeline layer ([Chapter 02](02-telemetry-architecture-instrumentation-and-pipelines.md)) versus
  buying a SaaS backend, or self-hosting an open-source backend such as
  Prometheus/Thanos/Mimir, Grafana Loki, and Grafana Tempo. Data
  residency, egress cost at telemetry volume, and existing vendor
  contracts typically decide this, not tooling preference.
- **Multi-tenancy model.** A shared observability platform needs tenant
  isolation (per business unit, per environment, or per compliance
  boundary) enforced at the storage and query layer, not by convention.
  Decide early whether tenancy is namespace-based (single cluster, label
  isolation) or cluster-based (physically separate stacks per regulated
  boundary); retrofitting isolation after data commingles is expensive and,
  for regulated data, may require a full re-ingest.
- **Ownership granularity.** Service-level ownership is coarser than
  team-level ownership in large orgs where one team runs many services, and
  finer than department-level ownership where accountability blurs.
  Encode ownership at the service (deployable unit) level in the catalog so
  it survives team reorganizations without a data migration.
- **Coverage gaps.** A service with no listed owner is not hypothetical —
  it is the normal state for anything built during a merger, an
  acquisition, or a deprecated-but-still-running system. The operating
  model must define what happens to an orphaned service (default owner,
  automatic tier downgrade, deprecation clock) rather than leaving it
  silently unpaged.
- **Governance versus autonomy tension.** Centralizing cost control,
  retention policy, and tagging taxonomy is necessary for a coherent
  platform; centralizing dashboard and alert *content* recreates the
  bottleneck the hybrid model exists to avoid. Draw the line at
  infrastructure and standards, not at content.

## Implementation and Automation

A service catalog is the operational backbone of the ownership model. It
can be implemented as a developer portal (for example, Backstage-style
`catalog-info.yaml` entries checked into each service's repository) or as a
lighter-weight YAML registry consumed by the observability platform's
onboarding automation. The essential fields are ownership, tier, and
escalation routing — everything else (documentation links, dependency
graphs) is additive value.

```yaml
# catalog-info.yaml — service ownership metadata, stored in the service repo
apiVersion: backstage.io/v1alpha1
kind: Component
metadata:
  name: checkout-api
  description: Authorizes and finalizes cart checkout
  tags:
    - tier-0
    - payments-domain
  annotations:
    pagerduty.com/service-id: "PXXXXXX"
    observability.internal/dashboard: "https://grafana.internal/d/checkout-api"
spec:
  type: service
  owner: group:payments-platform-team
  system: checkout
  lifecycle: production
  dependsOn:
    - component:payment-gateway-adapter
    - resource:checkout-postgres
```

Validate catalog completeness with a scheduled job rather than a manual
audit. The following script (safe to run against a Backstage-compatible
catalog API or an internal YAML registry) flags services missing required
ownership fields:

```bash
#!/usr/bin/env bash
# audit-catalog.sh — fail CI if a service is missing ownership metadata
set -euo pipefail

CATALOG_DIR="${1:-./catalog}"
missing=0

for f in "$CATALOG_DIR"/**/catalog-info.yaml; do
  owner=$(yq '.spec.owner' "$f")
  tier=$(yq '.metadata.tags[] | select(test("^tier-"))' "$f")
  pagerduty=$(yq '.metadata.annotations."pagerduty.com/service-id"' "$f")

  if [[ "$owner" == "null" || -z "$owner" ]]; then
    echo "MISSING OWNER: $f"
    missing=$((missing + 1))
  fi
  if [[ -z "$tier" ]]; then
    echo "MISSING TIER: $f"
    missing=$((missing + 1))
  fi
  if [[ "$pagerduty" == "null" ]]; then
    echo "MISSING ESCALATION ROUTE: $f"
    missing=$((missing + 1))
  fi
done

echo "Catalog audit complete: $missing issue(s) found"
exit "$missing"
```

Run `audit-catalog.sh` as a scheduled pipeline job (nightly) and as a
pre-merge check on any pull request touching `catalog-info.yaml`, so
ownership metadata cannot silently drift out of date the way it does when
tracked only in a wiki.

### Observability maturity model

Use a five-level maturity model to plan platform investment year over year
rather than chasing every new tool:

| Level | Characteristic | Typical next investment |
| --- | --- | --- |
| 0 — Reactive | Alerts only from infrastructure defaults; no service catalog | Stand up a service catalog and tiering |
| 1 — Instrumented | Services emit metrics/logs; no correlation | Adopt OpenTelemetry, shared trace context |
| 2 — Correlated | Metrics, logs, traces share identifiers | Define SLOs and error budgets ([Chapter 03](03-metrics-service-level-objectives-and-error-budgets.md)) |
| 3 — Proactive | SLO-driven alerting, blameless postmortems | Capacity forecasting, automated remediation |
| 4 — Predictive | Anomaly detection, automated runbooks, continual improvement loop closes findings back into design | Sustain and tune; avoid tool sprawl |

## Validation and Troubleshooting

- **Coverage audit.** Cross-reference the service catalog against the
  actual deployed inventory (Kubernetes namespaces, cloud resource tags, or
  a CMDB). Any deployed workload absent from the catalog is a coverage gap
  and, by definition, has no confirmed on-call owner.
- **Escalation path testing.** Periodically fire a synthetic test alert
  through each service's configured escalation policy (see [Chapter 06](06-actionable-alerting-on-call-and-operations-centers.md)) and
  confirm it reaches a human within the tier's target acknowledgment time.
  A catalog entry with a correct-looking PagerDuty service ID but a stale
  or empty on-call schedule behind it is a common silent failure.
- **Ownership drift after reorganizations.** Team renames and mergers are
  the most common cause of catalog rot. Tie the `owner` field to a
  directory-backed group identity (an IdP group, not a free-text team
  name) so a group rename propagates instead of orphaning every service
  that referenced the old name.
- **Symptom: pages routed to a defunct team distribution list.** Root
  cause is almost always a catalog entry that references a group deleted
  or renamed in the identity provider without a corresponding catalog
  update. Add IdP group deletion as a trigger for a catalog audit, not just
  a scheduled nightly run.

## Security and Best Practices

- Treat the service catalog itself as a sensitive asset: it maps
  organizational structure, on-call individuals, and system dependencies,
  which is reconnaissance value for an attacker planning a social
  engineering or timing-based attack. Restrict catalog write access to
  service owners and platform administrators; restrict catalog read access
  at minimum to authenticated internal users.
- Apply least privilege to the observability platform itself: read access
  to another team's dashboards and traces is often appropriate (it enables
  cross-service debugging), but write access to alert routing, retention
  configuration, and paging integrations should be scoped to the owning
  team plus platform administrators.
- Keep escalation policy credentials (paging API keys, webhook secrets) in
  a secrets manager referenced by the catalog, never inlined in
  `catalog-info.yaml` or any file committed to source control.
- Require a named human owner, not a team alias with no accountable
  individual, for every Tier 0 and Tier 1 service; alias-only ownership is
  a leading indicator of an unowned service during an audit.
- Log and periodically review changes to ownership, tiering, and
  escalation-routing metadata — an unauthorized tier downgrade is a
  realistic way to suppress paging ahead of a planned incident.

## References and Knowledge Checks

**References**

- [Google, *Site Reliability Engineering* and *The Site Reliability
  Workbook* (free online editions), particularly the chapters on
  monitoring philosophy and embedding SRE.](https://sre.google/sre-book/table-of-contents/)
- [Skelton, M. and Pais, M., *Team Topologies* (2019) for the
  stream-aligned/platform/enabling/complicated-subsystem vocabulary used
  in this chapter.](https://teamtopologies.com/book)
- [CNCF, *OpenTelemetry* project documentation, `opentelemetry.io`.](https://opentelemetry.io/docs/)
- [AXELOS/PeopleCert, *ITIL 4 Foundation* practice guides for service
  management vocabulary referenced throughout this volume.](https://www.peoplecert.org/browse-certifications/it-governance-and-service-management/ITIL-1/itil-4-foundation-2565)
- [Backstage (CNCF project) documentation, `backstage.io`, for the
  `catalog-info.yaml` schema used in this chapter's examples.](https://backstage.io/docs/)

**Knowledge Checks**

1. Explain, in one paragraph, why unbounded cardinality in modern
   distributed systems makes pre-declared dashboards insufficient on their
   own.
2. A 40-service organization currently runs a fully federated ownership
   model with no shared platform. Name two concrete symptoms you would
   expect to see, and the operating-model change that addresses each.
3. What three catalog fields are the minimum required to make a service
   both discoverable and pageable, and why does each matter?
4. Why should the observability platform team avoid owning individual
   dashboard content once product teams are onboarded?
5. Describe the failure mode caused by tying catalog ownership to a
   free-text team name instead of an identity-provider group.

## Hands-On Lab

**Objective:** Build a minimal, auditable service catalog for three
services and validate it with an automated completeness check.

### Prerequisites

- A POSIX shell (bash 5.x) and `yq` (Mike Farah's Go implementation, v4.x)
  installed locally.
- No production access required; this lab is entirely local files.

### Procedure

1. Create the working lab directory and a catalog subdirectory per
   service:

   ```bash
   mkdir -p ~/obs-lab/catalog/checkout-api \
            ~/obs-lab/catalog/inventory-service \
            ~/obs-lab/catalog/legacy-reporting
   cd ~/obs-lab
   ```

2. Create a complete catalog entry for `checkout-api`:

   ```bash
   cat > catalog/checkout-api/catalog-info.yaml <<'EOF'
   apiVersion: backstage.io/v1alpha1
   kind: Component
   metadata:
     name: checkout-api
     tags: ["tier-0"]
     annotations:
       pagerduty.com/service-id: "P1A2B3C"
   spec:
     type: service
     owner: group:payments-platform-team
     lifecycle: production
   EOF
   ```

3. Create a complete catalog entry for `inventory-service`:

   ```bash
   cat > catalog/inventory-service/catalog-info.yaml <<'EOF'
   apiVersion: backstage.io/v1alpha1
   kind: Component
   metadata:
     name: inventory-service
     tags: ["tier-1"]
     annotations:
       pagerduty.com/service-id: "P4D5E6F"
   spec:
     type: service
     owner: group:catalog-team
     lifecycle: production
   EOF
   ```

4. Create a deliberately incomplete entry for `legacy-reporting` (missing
   owner and escalation route), representing an unowned legacy system:

   ```bash
   cat > catalog/legacy-reporting/catalog-info.yaml <<'EOF'
   apiVersion: backstage.io/v1alpha1
   kind: Component
   metadata:
     name: legacy-reporting
     tags: ["tier-3"]
   spec:
     type: service
     lifecycle: deprecated
   EOF
   ```

5. Save the audit script from the Implementation and Automation section
   above as `audit-catalog.sh`, make it executable, and run it:

   ```bash
   chmod +x audit-catalog.sh
   ./audit-catalog.sh ./catalog
   ```

### Expected Results

The script prints `MISSING OWNER: ./catalog/legacy-reporting/catalog-info.yaml`
and `MISSING ESCALATION ROUTE: ./catalog/legacy-reporting/catalog-info.yaml`,
reports `Catalog audit complete: 2 issue(s) found`, and exits with a
non-zero status (`2`). `checkout-api` and `inventory-service` produce no
findings.

### Negative Test

Run `echo $?` immediately after the script exits. Confirm it returns `2`,
not `0` — a CI pipeline gate on this script must fail the build when
ownership metadata is incomplete. Then intentionally corrupt
`inventory-service`'s YAML (delete the closing `EOF` line effect by
truncating the file with `truncate -s -20 catalog/inventory-service/catalog-info.yaml`)
and re-run the script; confirm it errors clearly rather than silently
treating the service as compliant, and fix the script's YAML validation if
it does not.

### Cleanup

```bash
cd ~
rm -rf ~/obs-lab
```

## Summary and Completion Checklist

Observability is the ability to answer unanticipated questions from
existing telemetry, and it depends on an organizational model — not just
tooling — to succeed at enterprise scale. The hybrid platform-team-plus-
paved-road model, service ownership backed by a machine-readable catalog,
and tiering that drives operational rigor are the foundation the rest of
this volume builds on: telemetry pipelines ([Chapter 02](02-telemetry-architecture-instrumentation-and-pipelines.md)), SLOs ([Chapter 03](03-metrics-service-level-objectives-and-error-budgets.md)),
logging ([Chapter 04](04-enterprise-logging-event-management-and-retention.md)), tracing ([Chapter 05](05-distributed-tracing-profiling-and-dependency-analysis.md)), alerting ([Chapter 06](06-actionable-alerting-on-call-and-operations-centers.md)), incident
process ([Chapter 07](07-service-management-incident-problem-and-change-operations.md)), capacity and cost ([Chapter 08](08-capacity-performance-and-cost-aware-operations.md)), and automation
([Chapter 09](09-operational-automation-analytics-and-continual-improvement.md)) all assume a catalog exists and answers "who owns this."

**Completion checklist**

- [ ] Can articulate the difference between monitoring and observability
      and why cardinality drives the distinction.
- [ ] Can name the three observability operating models and the scale
      inflection points between them.
- [ ] Can define service tiering and explain how tier drives on-call and
      alerting rigor.
- [ ] Built and validated a minimal service catalog with an automated
      completeness audit.
- [ ] Understands the five-level observability maturity model and can
      place a hypothetical organization on it.
