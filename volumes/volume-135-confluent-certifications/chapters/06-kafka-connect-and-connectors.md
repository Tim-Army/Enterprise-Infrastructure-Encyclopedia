# Chapter 06: Kafka Connect and Connectors

## Learning Objectives

- Explain Kafka Connect's architecture: workers, connectors, tasks, and converters.
- Distinguish source from sink connectors, and standalone from distributed mode.
- Apply Single Message Transforms and dead-letter queues.
- Reason about connector parallelism and offset management.

## Why Connect exists

Most Kafka data comes from, or goes to, systems that are not Kafka: databases, object stores, search indexes, warehouses, SaaS APIs. Writing a bespoke producer or consumer for each integration means re-implementing the same concerns every time — offset tracking, restarts, scaling, retries, schema handling, error routing.

**Kafka Connect** is the framework that solves those once. You configure a connector declaratively (JSON) instead of writing integration code, and Connect handles the plumbing.

| Component | Role |
|:---|:---|
| **Worker** | The JVM process running connectors and tasks |
| **Connector** | The configuration and plan for moving data to/from an external system |
| **Task** | The unit of work and parallelism; a connector splits into tasks |
| **Converter** | Serialization between Kafka bytes and Connect's internal records (Avro, Protobuf, JSON, String) |
| **Transform (SMT)** | Lightweight per-record modification in the pipeline |

**Source** connectors bring data *into* Kafka (database change data capture, files, APIs). **Sink** connectors push data *out* (to warehouses, object storage, search).

## Standalone versus distributed

| Mode | Fits | Trade-off |
|:---|:---|:---|
| **Standalone** | Development, single-machine cases | No fault tolerance; offsets in a local file |
| **Distributed** | Production | Workers form a cluster, tasks rebalance on failure, offsets and configs live in Kafka topics |

Distributed mode stores its state — configs, offsets, status — in internal Kafka topics, which is why a worker can die and its tasks resume elsewhere without losing position.

## Parallelism

`tasks.max` requests parallelism, but the connector decides what it can actually use: a source connector reading 4 database tables can usefully split into at most 4 tasks; a sink connector is bounded by the **partition count** of the topics it consumes, exactly as any consumer group is (Chapter 04). Requesting 20 tasks for a 3-partition topic produces 3 working tasks and 17 idle ones.

## Transforms and error handling

**Single Message Transforms (SMTs)** modify records in flight — mask a field, rename it, route by content, add a timestamp, cast a type. They are for *lightweight* per-record work; anything involving joins, aggregation, or state belongs in stream processing (Chapter 07).

**Dead-letter queues** decide what happens to a record Connect cannot process:

| `errors.tolerance` | Behavior |
|:---|:---|
| `none` (default) | Fail the task — the pipeline stops on the first bad record |
| `all` + DLQ topic | Route bad records to a dead-letter topic and keep going |

The default stops everything for one malformed record, which is rarely what you want in production; a DLQ keeps the pipeline flowing and preserves the failures for inspection. But a DLQ nobody monitors is a silent data-loss channel — the failures accumulate unseen.

## Hands-On Lab

Python models Connect. **Cost:** none.

### Lab 6.1 — Model a connector pipeline with tasks

**Objective:** Show how connectors split into tasks and where parallelism caps.

```bash
python3 - <<'EOF'
def plan(name, kind, tasks_max, work_units, topic_partitions=None):
    if kind == "source":
        actual = min(tasks_max, work_units)
        cap = f"work units available ({work_units} tables/files)"
    else:
        actual = min(tasks_max, topic_partitions)
        cap = f"topic partitions ({topic_partitions})"
    print(f"\n{name} [{kind}]  tasks.max={tasks_max}")
    print(f"   running tasks: {actual}   (capped by {cap})")
    if actual < tasks_max:
        print(f"   {tasks_max - actual} requested task(s) IDLE — tasks.max is a request, not a guarantee")
    for t in range(actual):
        print(f"      task-{t}: assigned work")

plan("jdbc-source-orders",  "source", tasks_max=8,  work_units=4)
plan("s3-sink-events",      "sink",   tasks_max=20, work_units=0, topic_partitions=3)
plan("s3-sink-events (fixed)","sink", tasks_max=3,  work_units=0, topic_partitions=3)
EOF
```

**Expected result:** The JDBC source runs 4 tasks (one per table) despite requesting 8, and the S3 sink runs 3 despite requesting 20 — capped by topic partitions, the same rule that governs consumer groups. `tasks.max` is a **ceiling request**, and over-requesting produces idle tasks rather than more throughput. To genuinely parallelize a sink, add partitions to the source topic.

**Negative test:** Raising `tasks.max` to fix a slow sink — throughput does not change, because the partition count is the real constraint.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 6.2 — Single Message Transforms

**Objective:** Chain SMTs and see where their limits are.

```bash
python3 - <<'EOF'
def mask_field(rec, field):   return {**rec, field: "****"} if field in rec else rec
def rename_field(rec, a, b):  return {b: v for k, v in rec.items() for b in [b if k == a else k]}
def add_timestamp(rec, ts):   return {**rec, "ingested_at": ts}
def route(rec, field):        return f"orders.{rec.get(field,'unknown')}"

record = {"order_id":"o-1","cust_ssn":"123-45-6789","amount":42.5,"region":"emea"}
print(f"raw            : {record}")
r = mask_field(record, "cust_ssn");        print(f"MaskField      : {r}")
r = rename_field(r, "order_id", "id");     print(f"RenameField    : {r}")
r = add_timestamp(r, "2026-08-04T11:00Z"); print(f"InsertField    : {r}")
print(f"topic routing  : {route(r, 'region')}")
print("\nSMTs are PER-RECORD and stateless — masking, renaming, routing, casting.")
print("They CANNOT join, aggregate, or window: that needs Kafka Streams or Flink (ch07).")
print("Masking at ingest is the useful pattern here — sensitive data never lands in the topic.")
EOF
```

**Expected result:** A chain masks the SSN, renames a field, adds a timestamp, and routes by region. The important boundary is stated at the end: SMTs are **stateless and per-record**, so anything requiring memory of other records belongs in stream processing. The masking example is worth noting as a genuine security pattern — transforming at ingest means the sensitive value never reaches the topic at all, rather than being redacted downstream.

**Negative test:** Trying to deduplicate or aggregate with SMTs — they see one record at a time with no state, so it cannot be done there regardless of how the transform is written.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 6.3 — Dead-letter queues and error tolerance

**Objective:** Keep a pipeline running without losing failures silently.

```bash
python3 - <<'EOF'
def run_pipeline(records, tolerance, dlq_enabled, dlq_monitored):
    delivered, dlq, stopped_at = [], [], None
    for i, r in enumerate(records):
        bad = not isinstance(r.get("amount"), (int, float))
        if not bad:
            delivered.append(r); continue
        if tolerance == "none":
            stopped_at = i; break
        dlq.append(r) if dlq_enabled else None
    return delivered, dlq, stopped_at

records = [{"id":1,"amount":10.0},{"id":2,"amount":"NaN"},{"id":3,"amount":30.0},{"id":4,"amount":40.0}]

for tol, dlq_on, monitored in [("none", False, False), ("all", False, False), ("all", True, False), ("all", True, True)]:
    d, q, stop = run_pipeline(records, tol, dlq_on, monitored)
    print(f"\ntolerance={tol:5} dlq={str(dlq_on):5} monitored={str(monitored):5}")
    print(f"   delivered={len(d)}/{len(records)}" + (f"  TASK FAILED at record index {stop}" if stop is not None else ""))
    if tol == "all" and not dlq_on:
        print("   bad record DROPPED silently — data loss with no record of it")
    elif q:
        print(f"   {len(q)} record(s) in DLQ" + ("  (alerting on DLQ depth — failures get seen)" if monitored
              else "  <-- DLQ NOT MONITORED: this is silent data loss with extra steps"))
EOF
```

**Expected result:** The default `none` stops the whole pipeline at the first bad record (1 of 4 delivered); `all` without a DLQ drops it silently; `all` with an unmonitored DLQ preserves it where nobody looks; only the last configuration both keeps the pipeline running and surfaces the failure. The middle two rows are the trap — they *look* like resilience while quietly losing data.

**Negative test:** Configuring a DLQ and never alerting on its depth — you have converted a loud failure into a silent one, which is worse than the default because it removes the signal that something is wrong.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] Connect architecture described: workers, connectors, tasks, converters, transforms.
- [ ] Source vs sink and standalone vs distributed distinguished.
- [ ] Task parallelism modeled, with sinks capped by partition count.
- [ ] SMTs applied for per-record work, with their stateless limit understood.
- [ ] Dead-letter queues configured *and* monitored, avoiding silent loss.
