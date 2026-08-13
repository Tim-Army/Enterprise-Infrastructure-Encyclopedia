# Chapter 04: Consumers and Consumer Groups

## Learning Objectives

- Explain consumer groups, partition assignment, and why parallelism is capped.
- Choose an offset commit strategy and know what each risks.
- Measure and interpret consumer lag.
- Understand rebalancing and how to keep it from hurting.

## Consumer groups

A **consumer group** is a set of consumers sharing a `group.id` that cooperatively consume a topic. The rule that governs everything:

> **Each partition is assigned to exactly one consumer in the group.**

Which gives the constraint people meet immediately in production:

- Consumers ≤ partitions → every consumer gets work.
- Consumers > partitions → **the surplus consumers sit idle**. You cannot scale a group beyond the partition count.

Different groups are independent: each maintains its own offsets, so the same topic can feed an analytics pipeline, an audit sink, and a real-time service simultaneously, each at its own position.

## Offsets and commit strategy

A consumer tracks its position with a **committed offset**, stored in Kafka's internal `__consumer_offsets` topic. When and how you commit decides your delivery semantics on the consuming side:

| Strategy | Behavior | Risk |
|:---|:---|:---|
| **Auto-commit** (`enable.auto.commit=true`) | Commits periodically in the background | Can commit records you have not finished processing → **loss** |
| **Manual commit after processing** | Commit once work succeeds | **Duplicates** on crash between processing and commit (at-least-once) |
| **Manual commit before processing** | Commit on receipt | **Loss** if processing then fails (at-most-once) |
| **Transactional** (Chapter 03) | Offsets committed with outputs atomically | Exactly-once, with more machinery |

The default at-least-once approach is manual commit after processing — accept possible duplicates and make your processing **idempotent** downstream.

## Lag

**Consumer lag** = latest offset in the partition − committed offset: how far behind the consumer is, in records. It is the single most important consumer health metric, and what matters is its **trend**:

- Lag stable near zero → keeping up.
- Lag stable but large → keeping up *now*, but recovering from a backlog slowly (or never).
- **Lag growing** → the consumer is slower than the producer, and it will never catch up without intervention.

## Rebalancing

When group membership changes — a consumer joins, leaves, or is presumed dead — partitions are reassigned in a **rebalance**. Under the classic eager protocol, everyone stops consuming while it happens ("stop-the-world"). **Cooperative incremental rebalancing** reassigns only the affected partitions, letting other consumers keep working.

The usual self-inflicted cause of rebalances: a consumer whose processing loop takes longer than `max.poll.interval.ms`, so the group presumes it dead and rebalances — which slows everyone, making timeouts more likely. Either process faster, reduce `max.poll.records`, or raise the interval.

## Hands-On Lab

Python models consumer groups. **Cost:** none.

### Lab 4.1 — Partition assignment and the parallelism cap

**Objective:** Show why extra consumers do nothing.

```bash
python3 - <<'EOF'
def assign(partitions, consumers):
    a = {c: [] for c in consumers}
    for i, p in enumerate(partitions):
        a[consumers[i % len(consumers)]].append(p)
    return a

partitions = list(range(6))
for n in (2, 3, 6, 8):
    consumers = [f"c{i}" for i in range(n)]
    a = assign(partitions, consumers)
    idle = [c for c, ps in a.items() if not ps]
    print(f"\n6 partitions, {n} consumers:")
    for c, ps in a.items():
        print(f"   {c}: partitions {ps}" + ("   <-- IDLE" if not ps else ""))
    if idle:
        print(f"   {len(idle)} consumer(s) IDLE — parallelism is capped at the PARTITION count")
EOF
```

**Expected result:** With 6 partitions, 2 consumers take 3 each, 6 take 1 each, and **8 leaves 2 completely idle**. Scaling a consumer group past the partition count buys nothing — the fix is more partitions, which must be planned in advance (Chapter 02's remapping caveat). This is the most common surprise for teams who scale a deployment and see no throughput change.

**Negative test:** Autoscaling consumers on CPU with no regard for partition count — the platform launches pods that join the group, sit idle, and trigger a rebalance each time they arrive.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 4.2 — Commit strategies and their failure modes

**Objective:** Model loss versus duplication.

```bash
python3 - <<'EOF'
def run(strategy, crash_after_processing):
    processed, committed = [], None
    records = [("r1",10),("r2",11),("r3",12)]
    for rec, off in records:
        if strategy == "commit-before":
            committed = off
            if crash_after_processing and rec == "r2":
                return processed, committed, "CRASH — r2 committed but never processed -> LOST"
            processed.append(rec)
        elif strategy == "commit-after":
            processed.append(rec)
            if crash_after_processing and rec == "r2":
                return processed, committed, "CRASH — r2 processed but not committed -> REPROCESSED (duplicate)"
            committed = off
        else:  # auto-commit on a timer
            if rec == "r2" and crash_after_processing:
                committed = off
                return processed, committed, "CRASH — timer committed r2 mid-processing -> LOST"
            processed.append(rec); committed = off
    return processed, committed, "clean run"

for s in ("commit-before","commit-after","auto-commit"):
    p, c, note = run(s, True)
    print(f"{s:14} processed={p}  committed_offset={c}\n{'':14} -> {note}\n")
print("commit-after (at-least-once) is the usual choice: duplicates are survivable if")
print("your processing is idempotent; silent loss usually is not.")
EOF
```

**Expected result:** Commit-before and auto-commit both **lose** `r2`; commit-after **reprocesses** it. The recommendation follows from asymmetry of consequences — a duplicate you can design around with idempotent processing, whereas silent loss is typically discovered much later by reconciliation, if at all.

**Negative test:** Leaving auto-commit enabled in a consumer doing slow processing — the background timer commits offsets for records still in flight, and a crash loses them with no error.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 4.3 — Read consumer lag correctly

**Objective:** Distinguish healthy lag from a consumer that will never catch up.

```bash
python3 - <<'EOF'
histories = {
  "orders-consumer":    [120, 118, 125, 119, 122],       # stable, small
  "analytics-consumer": [5000, 5200, 5400, 5600, 5800],  # growing
  "audit-consumer":     [90000, 72000, 55000, 38000, 21000],  # draining a backlog
  "idle-consumer":      [0, 0, 0, 0, 0],
}
for name, lag in histories.items():
    delta = lag[-1] - lag[0]
    rate = delta / (len(lag) - 1)
    if rate > 10:
        verdict = f"GROWING (+{rate:.0f}/interval) — consumer is slower than the producer; it will NEVER catch up"
    elif rate < -10:
        eta = lag[-1] / abs(rate)
        verdict = f"DRAINING ({rate:.0f}/interval) — backlog clears in ~{eta:.0f} intervals"
    elif lag[-1] > 1000:
        verdict = "STABLE but LARGE — keeping pace, not recovering; latency is permanently high"
    else:
        verdict = "HEALTHY — keeping up"
    print(f"{name:20} lag {lag[0]:>6} -> {lag[-1]:<6} {verdict}")
print("\nAlert on lag TREND, not an absolute number: 5,000 draining is fine; 5,000 growing is an outage forming.")
EOF
```

**Expected result:** Four distinct diagnoses from lag alone — healthy, **growing** (an outage in the making), draining a backlog with an ETA, and stable-but-large. The closing rule is the operationally useful one: alerting on an absolute lag threshold pages you for a harmless backlog drain and stays quiet while a slowly growing lag becomes unrecoverable. Trend is the signal.

**Negative test:** Alerting at "lag > 1000" — the audit consumer pages constantly while healthily draining, and the analytics consumer stays under the threshold for hours while diverging.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] Consumer-group assignment modeled, with parallelism capped at partition count.
- [ ] Commit strategies compared by failure mode; commit-after chosen with idempotent processing.
- [ ] Consumer lag interpreted by trend rather than absolute value.
- [ ] Rebalancing causes understood, including `max.poll.interval.ms` timeouts.
