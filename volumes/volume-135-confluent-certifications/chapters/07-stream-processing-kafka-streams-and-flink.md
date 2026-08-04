# Chapter 07: Stream Processing — Kafka Streams and Flink

## Learning Objectives

- Build stream-processing topologies from stateless and stateful operations.
- Apply windowing and understand event time versus processing time.
- Explain state stores, changelogs, and how they survive failure.
- Place Apache Flink alongside Kafka Streams, including the new accreditation.

## Two ways to process streams

| | **Kafka Streams** | **Apache Flink** |
|:---|:---|:---|
| What it is | A **Java library** you embed in your application | A **distributed processing engine** with its own cluster |
| Deployment | Just your app — scale by running more instances | A Flink cluster (or Confluent's managed Flink) |
| Scope | Kafka-to-Kafka | Many sources and sinks; batch and streaming |
| Certification | Part of **CCDAK** (Stream Processing using Kafka Streams is on the developer path) | **Fundamentals Accreditation for Apache Flink** (free, new) |

Kafka Streams' defining virtue is that there is no separate cluster: your stream processor is an ordinary application that happens to consume, transform, and produce. Flink brings a full engine with richer windowing, event-time handling, and non-Kafka connectivity — and Confluent's new free Flink accreditation signals how central it has become to their platform.

## Stateless and stateful operations

| Kind | Operations | Needs state? |
|:---|:---|:---|
| **Stateless** | `filter`, `map`, `flatMap`, `branch`, `peek` | No — each record independently |
| **Stateful** | `count`, `aggregate`, `reduce`, joins, windowing | **Yes** — memory of previous records |

Stateful operations require **state stores**, which live locally with the processing instance (RocksDB by default) and are **backed by changelog topics in Kafka**. That backing is what makes the state durable: if an instance dies, another rebuilds the store by replaying the changelog. Streaming state is not lost on restart — it is re-derived from the log, which is the same principle that makes the log valuable everywhere else.

## Streams and tables

A core duality worth internalizing: a **stream** is a sequence of events (each record an independent fact), while a **table** is the current state per key (each record an update). They convert into each other — aggregating a stream produces a table; capturing changes to a table produces a stream. **Log compaction** (Chapter 02) is exactly the table view of a topic: keep the latest value per key.

## Time and windowing

Windows bound a stateful computation to a period. The critical distinction:

- **Event time** — when the event actually happened, per its embedded timestamp.
- **Processing time** — when your processor happened to see it.

They differ whenever data is delayed — mobile clients reconnecting, batch uploads, network partitions, replays. **Correct results require event time**, because a record from 10:59 that arrives at 11:05 belongs in the 10:00–11:00 window regardless of when you saw it.

| Window type | Shape |
|:---|:---|
| **Tumbling** | Fixed, non-overlapping (every 5 minutes) |
| **Hopping** | Fixed size, overlapping (5-minute window every 1 minute) |
| **Sliding** | Defined by record proximity within a duration |
| **Session** | Bounded by inactivity gaps — natural for user sessions |

**Late data** is the practical complication: a **grace period** keeps a window open for stragglers, and records arriving after it are dropped or routed aside. Longer grace means more correctness and more retained state.

## Hands-On Lab

Python models stream processing. **Cost:** none.

### Lab 7.1 — Build a topology: stateless then stateful

**Objective:** Compose operations and see where state enters.

```bash
python3 - <<'EOF'
events = [
  {"user":"u1","action":"view","amount":0},
  {"user":"u1","action":"purchase","amount":50},
  {"user":"u2","action":"purchase","amount":30},
  {"user":"u1","action":"purchase","amount":20},
  {"user":"u3","action":"view","amount":0},
]
# STATELESS: filter -> map (no memory needed)
purchases = [e for e in events if e["action"] == "purchase"]          # filter
enriched  = [{**e, "amount_cents": e["amount"]*100} for e in purchases]  # map
print("stateless (filter -> map):")
for e in enriched: print(f"   {e}")

# STATEFUL: aggregate per key (needs a state store)
state = {}
print("\nstateful (groupByKey -> aggregate) — state store evolves per record:")
for e in enriched:
    state[e["user"]] = state.get(e["user"], 0) + e["amount"]
    print(f"   after {e['user']} +{e['amount']:>3}: state={state}")
print(f"\nfinal table: {state}")
print("\nThe state store is local (RocksDB) and backed by a CHANGELOG topic in Kafka,")
print("so a crashed instance's state is rebuilt by replaying that changelog elsewhere.")
EOF
```

**Expected result:** Filter and map need no memory; the per-user aggregation builds state incrementally into a table (`u1: 70, u2: 30`). The closing note is the durability story that makes stateful streaming viable: state is local for speed but **changelog-backed in Kafka** for recovery, so a lost instance costs a replay rather than the state itself.

**Negative test:** Keeping aggregation state only in application memory with no changelog — an instance restart loses every running total, and there is no way to reconstruct them.

**Cleanup:** None.

### Lab 7.2 — Event time versus processing time

**Objective:** Show why processing time gives wrong answers.

```bash
python3 - <<'EOF'
# (event_time, processing_time, value) — one mobile client was offline and uploaded late
records = [
  ("10:15","10:15", 10),
  ("10:45","10:45", 20),
  ("10:59","11:05", 30),   # LATE: happened at 10:59, seen at 11:05
  ("11:10","11:10", 40),
]
def window_of(t): return "10:00-11:00" if t < "11:00" else "11:00-12:00"

for label, idx in (("PROCESSING time", 1), ("EVENT time", 0)):
    buckets = {}
    for r in records:
        buckets.setdefault(window_of(r[idx]), []).append(r[2])
    print(f"{label}:")
    for w, vals in sorted(buckets.items()):
        print(f"   {w}: {vals} = {sum(vals)}")
    print()
print("The 10:59 record (value 30) belongs to the 10:00-11:00 hour.")
print("Processing time puts it in 11:00-12:00 — BOTH hourly totals are wrong.")
print("Event time is required for correctness; a GRACE PERIOD keeps the window open for stragglers.")
EOF
```

**Expected result:** Processing time reports 30 and 70; event time reports the correct 60 and 40. One late record corrupts **two** windows — the one it should have joined and the one it wrongly landed in. This is the argument for event-time semantics, and the reason grace periods exist: the window must stay open long enough for realistic lateness.

**Negative test:** Using processing time because it is simpler — the results look plausible and are quietly wrong whenever the network, a mobile client, or a replay introduces delay, which is always.

**Cleanup:** None.

### Lab 7.3 — Windowed aggregation with a grace period

**Objective:** Handle late arrivals explicitly.

```bash
python3 - <<'EOF'
WINDOW_MIN, GRACE_MIN = 10, 5
def window_start(minute): return (minute // WINDOW_MIN) * WINDOW_MIN

records = [(3, 5), (7, 5), (12, 8), (9, 4), (18, 9), (8, 6)]   # (event_minute, value)
windows, dropped, stream_time = {}, [], 0

for minute, value in records:
    stream_time = max(stream_time, minute)                     # advances with observed events
    ws = window_start(minute)
    window_close = ws + WINDOW_MIN + GRACE_MIN
    if stream_time > window_close:
        dropped.append((minute, value))
        print(f"event t={minute:>2} value={value}: window [{ws},{ws+WINDOW_MIN}) closed at t={window_close} "
              f"(stream time {stream_time}) -> DROPPED as too late")
        continue
    windows.setdefault(ws, []).append(value)
    late = " (late but within grace)" if minute < stream_time else ""
    print(f"event t={minute:>2} value={value}: -> window [{ws},{ws+WINDOW_MIN}){late}")

print("\nfinal windows:")
for ws, vals in sorted(windows.items()):
    print(f"   [{ws},{ws+WINDOW_MIN}): {vals} = {sum(vals)}")
print(f"dropped as too late: {dropped}")
print(f"\nGrace of {GRACE_MIN} min admitted the t=9 straggler but rejected t=8 once stream time reached 18.")
print("Longer grace = more correctness, more state retained. It is a deliberate trade, not a default.")
EOF
```

**Expected result:** The `t=9` record arrives after `t=12` but lands correctly in the `[0,10)` window because the grace period is still open; `t=8`, arriving once stream time reaches 18, is **dropped as too late**. That contrast is the lesson — grace is a bounded tolerance, not unlimited patience, and its length is a conscious trade between correctness and retained state.

**Negative test:** Setting grace to zero for lower memory use — every straggler is dropped, so windowed totals silently under-count whenever anything is delayed.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] Kafka Streams (embedded library) and Flink (distributed engine) distinguished, with the free Flink accreditation noted.
- [ ] Stateless and stateful operations separated, with changelog-backed state stores explained.
- [ ] Stream–table duality and its link to log compaction understood.
- [ ] Event time preferred over processing time, and windowing types applied.
- [ ] Grace periods used to admit late data as an explicit correctness/state trade.
