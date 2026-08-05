# Chapter 02: Telemetry, Agents, Entities, and Workloads

## Learning Objectives

- Distinguish the four MELT telemetry types and choose the right one per question.
- Place APM agents, the infrastructure agent, and integrations in the collection picture.
- Organize an estate with entities, tags, and workloads.
- Add custom attributes so telemetry answers business questions, not just technical ones.

*Exam relevance: NVF Section 1 (Observability Fundamentals — "core telemetry data types and monitoring agents"), Section 3 (Configuring Data — "instrumentation concepts… custom data and attributes, manage data through entities, tags, and workloads"), and APA Section 2 (Managing Agent Data — "instrumenting applications using APM agents, setting up application names, configuration settings, and tagging").*

## MELT: four telemetry types

New Relic's data model names four types — **metrics, events, logs, traces** — and everything the platform does rests on sending each question to the right one:

| Type | Shape | Best at | Weak at |
|:---|:---|:---|:---|
| **Metrics** | Aggregated numeric series | Trends, rates, cheap long retention | Per-request detail |
| **Events** | One record per occurrence, arbitrary attributes | "Show me each transaction that…" | Long-window aggregation cost |
| **Logs** | Text records, parsed attributes | What a component said at the time | Cross-service structure |
| **Traces** | Spans linked across services | Where one request spent its time | Aggregate trends |

The New Relic twist on this familiar table is that **events are first-class**. An APM agent records a `Transaction` event per request, with attributes, and NRQL queries it directly — which is why questions that need per-occurrence precision ("every transaction over 2 s for this customer") are natural here, and why Chapter 03's cost discipline matters: per-occurrence data is the expensive kind.

## Who collects what

| Collector | Produces | Notes |
|:---|:---|:---|
| **APM agents** (per-language) | Transactions, errors, traces, app metrics | Auto-instrument supported frameworks |
| **Infrastructure agent** | Host metrics, process data, events | Also hosts **on-host integrations** |
| **On-host / cloud integrations** | Service-specific telemetry (databases, queues, cloud APIs) | Ride on the infra agent or poll cloud providers |
| **Browser / mobile agents** | Front-end telemetry | Chapter 05 |
| **OpenTelemetry** | Anything OTLP | New Relic ingests OTel natively |

The same silent-gap caution from [Volume CXL](../../volume-140-dynatrace-certifications/chapters/02-oneagent-activegate-and-deployment.md) applies to any auto-instrumenting agent: what the agent does not cover is *absent*, not *errored*. The reconciliation habit — detected services checked against a maintained inventory — transfers to New Relic unchanged, so this volume does not repeat the lab; it repeats the instruction.

**Application naming** is APA material and worth taking seriously: the app name is the identity under which everything aggregates. Naming per environment (`checkout-prod`, `checkout-staging`) keeps signals separate; letting both report as `checkout` merges staging noise into production baselines and no tool downstream can fully separate them.

## Entities, tags, workloads

Everything reporting to New Relic becomes an **entity** — an app, host, service, monitor, dashboard — with a GUID and metadata. Organization happens in two layers:

- **Tags** attach key-value classification (`team:payments`, `env:prod`, `tier:1`). As in every platform on this shelf, rule-derived tags (from cloud metadata, Kubernetes labels, agent config) age well; hand-applied ones rot.
- **Workloads** group entities into a named unit — "everything the checkout flow depends on" — with rolled-up health. A workload is the difference between "which of our 400 entities are unhealthy?" and "is *checkout* healthy?", which is the question someone actually asked.

The NVF topics name entities, tags, and workloads explicitly, and the exam-visible skill is knowing **which layer answers which question**: tags filter and slice; workloads aggregate to a business-meaningful unit.

## Custom attributes

Agents accept **custom attributes** on transactions and events — `customer_tier`, `order_value`, `feature_flag`. This is the cheapest high-leverage instrumentation change most teams never make: with `customer_tier` on every transaction, "are premium customers seeing more errors than free ones?" becomes a one-line NRQL query instead of a correlation project.

The discipline that keeps it safe is the same pair of rules from the DEM chapters of Volumes CXXXIX and CXL: **bounded values only** (tiers, flags, categories — never raw IDs into anything metric-shaped) and **no sensitive data** — an attribute is telemetry, retained and queryable, not a scratchpad.

## Hands-On Lab

Python models the data model. **Cost:** none.

### Lab 2.1 — Send each question to the right telemetry type

**Objective:** Practice the MELT routing decision.

```bash
python3 - <<'EOF'
QUESTIONS = [
  ("What is checkout's p95 latency trend over 90 days?",        "metrics",
   "aggregated series; cheap at long retention"),
  ("Show every transaction >2s for customer tier 'premium'",     "events",
   "per-occurrence records with attributes"),
  ("Why did THIS request take 4 seconds across 6 services?",     "traces",
   "one request's path, span by span"),
  ("What did the payment service log during the 10:04 spike?",   "logs",
   "component-local detail at a point in time"),
  ("Is error rate rising faster than traffic?",                  "metrics",
   "two rates compared — aggregation, not detail"),
  ("Which feature flag was on for the failing requests?",        "events",
   "per-occurrence attribute filtering"),
]
print(f"{'question':58}{'type':>9}   why")
for q, t, why in QUESTIONS:
    print(f"{q:58}{t:>9}   {why}")

print("\nThe pattern: AGGREGATE questions -> metrics. PER-OCCURRENCE questions ->")
print("events (or traces when the occurrence spans services; logs when you need")
print("what one component said). New Relic makes events unusually capable — a")
print("Transaction event per request, queryable in NRQL — which is powerful and")
print("is also why Chapter 03 spends time on what per-occurrence data costs.")
EOF
```

**Expected result:** Six questions routed across all four types, with both aggregate questions landing on metrics. The routing rule in the closing block is the reusable part — aggregate versus per-occurrence is the first fork, and the other three types split the per-occurrence cases by scope.

**Negative test:** Answering the 90-day trend question from Transaction events. It works, and it scans ninety days of per-request records to produce twelve numbers a metric already held.

**Cleanup:** None.

### Lab 2.2 — Tags slice, workloads answer

**Objective:** Model the two organizational layers doing their different jobs.

```bash
python3 - <<'EOF'
ENTITIES = [
  # name,             type,      tags,                                health
  ("checkout-api",    "APM app", {"team":"payments","env":"prod","tier":"1"}, "healthy"),
  ("payment-svc",     "APM app", {"team":"payments","env":"prod","tier":"1"}, "DEGRADED"),
  ("checkout-db",     "on-host", {"team":"payments","env":"prod","tier":"1"}, "healthy"),
  ("checkout-web",    "browser", {"team":"payments","env":"prod","tier":"1"}, "healthy"),
  ("search-api",      "APM app", {"team":"search","env":"prod","tier":"2"},   "healthy"),
  ("search-api-stg",  "APM app", {"team":"search","env":"staging","tier":"2"},"DEGRADED"),
  ("recs-api",        "APM app", {"team":"ml","env":"prod","tier":"2"},       "healthy"),
]
WORKLOADS = {
  "Checkout flow": lambda e: e[2].get("team")=="payments" and e[2].get("env")=="prod",
}
def slice_by(key, val):
    return [e[0] for e in ENTITIES if e[2].get(key)==val]

print("TAGS slice the estate:")
print(f"   env:prod        -> {len(slice_by('env','prod'))} entities")
print(f"   team:payments   -> {', '.join(slice_by('team','payments'))}")
print(f"   tier:1          -> {len(slice_by('tier','1'))} entities")

print("\nWORKLOAD rolls up to the question someone asked:")
for workload_name, rule in WORKLOADS.items():
    members = [e for e in ENTITIES if rule(e)]
    bad = [e[0] for e in members if e[3] != "healthy"]
    status = f"DEGRADED (because: {', '.join(bad)})" if bad else "healthy"
    print(f"   '{workload_name}' ({len(members)} entities) -> {status}")

print("\nNote what the workload did that a tag filter cannot: it gave ONE answer")
print("with a reason. 'Is checkout healthy?' -> 'No, payment-svc.' A tag filter")
print("returns a list; a workload returns a verdict.")
print("\nAlso note search-api-stg is degraded and NO ONE is paged: it is staging,")
print("and it is in no production workload. Correct by construction — because env")
print("is a tag, not part of a hand-maintained list.")
EOF
```

**Expected result:** Tag slices return entity lists; the Checkout workload returns "DEGRADED (because: payment-svc)". The verdict-versus-list distinction is what the NVF topics are getting at when they name both features — and the staging entity degrading without consequence shows rule-based membership doing quiet, correct work.

**Negative test:** Building the workload as a hand-picked entity list. The next service the payments team ships is silently outside it.

**Cleanup:** None.

### Lab 2.3 — Custom attributes pay for themselves

**Objective:** Show the before/after of one attribute.

```bash
python3 - <<'EOF'
import random
random.seed(9)
# Transactions WITHOUT and WITH a customer_tier custom attribute
sampled = []
for i in range(5000):
    tier = random.choices(["free","pro","enterprise"], weights=[70,25,5])[0]
    err = random.random() < ({"free":0.006,"pro":0.008,"enterprise":0.031}[tier])
    sampled.append({"tier":tier, "error":err})

print("Question from support: 'enterprise customers say checkout is failing — true?'\n")
overall = sum(t["error"] for t in sampled)/len(sampled)*100
print(f"WITHOUT the attribute: overall error rate = {overall:.2f}%")
print("   -> looks fine; the enterprise signal is drowned by free-tier volume.")
print("   -> answering means joining payment logs to a CRM export. Days.\n")

print("WITH customer_tier on every Transaction event (one agent config line):")
print("   NRQL: SELECT percentage(count(*), WHERE error IS true)")
print("         FROM Transaction FACET customer_tier\n")
for tier in ("free","pro","enterprise"):
    sub = [t for t in sampled if t["tier"]==tier]
    rate = sum(t["error"] for t in sub)/len(sub)*100
    flag = "   <-- the complaint is REAL and invisible in the overall rate" if tier=="enterprise" else ""
    print(f"   {tier:12} {rate:5.2f}%  ({len(sub):,} sampled){flag}")

ent = [t for t in sampled if t["tier"]=="enterprise"]
ratio = (sum(t["error"] for t in ent)/len(ent)) / (sum(t["error"] for t in sampled)/len(sampled))
print(f"\nThe overall rate hid a {ratio:.0f}x elevation for the smallest, most valuable segment.")
print("Rules for attributes that stay safe:")
print("   BOUNDED values only — tiers, flags, categories; never raw user IDs")
print("   NO sensitive data — an attribute is retained, queryable telemetry")
EOF
```

**Expected result:** An overall error rate of 0.84% concealing a 4.05% enterprise-tier rate — real, roughly 5x elevated, and invisible without the attribute. The economics are the lesson: one configuration line converts a multi-day support investigation into a one-line FACET query, which is why custom attributes are the highest-leverage instrumentation change on the APA syllabus.

**Negative test:** Adding `customer_id` instead of `customer_tier` "for more detail." Unbounded values, cardinality bill, and a privacy review — the bounded version answered the question.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] MELT types matched to aggregate versus per-occurrence questions.
- [ ] Agents, integrations, and OpenTelemetry ingest placed; application naming treated as identity.
- [ ] Tags used to slice; workloads used to return verdicts.
- [ ] Custom attributes added with bounded values and no sensitive data.
