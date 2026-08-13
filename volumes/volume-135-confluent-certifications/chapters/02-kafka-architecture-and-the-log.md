# Chapter 02: Kafka Architecture and the Partitioned Log

## Learning Objectives

- Explain the partitioned, append-only log and why offsets are per-partition.
- Describe brokers, topics, partitions, replication, leaders, and the ISR.
- Reason about ordering guarantees and what partitioning costs you.
- Choose partition counts and replication factors deliberately.

## The log is the whole idea

Kafka's core abstraction is a **topic**: a named stream of events, physically stored as one or more **partitions**. Each partition is an **append-only, immutable, ordered log**, and each record in it has a monotonically increasing **offset**.

Three consequences follow, and they explain almost everything about Kafka:

1. **Appending is fast.** Writes go to the end of a file; no random access, no in-place update.
2. **Reading is independent.** Consumers track their own offset, so many consumers read the same data at different positions without interfering. Reading is not destructive.
3. **Ordering is per-partition, not per-topic.** This is the single most consequential fact in Kafka.

## Partitions, keys, and ordering

Kafka guarantees ordering **within a partition** — not across a topic. A producer chooses the partition either explicitly, by **key hashing** (same key → same partition), or round-robin when there is no key.

So if order matters for a given entity — all events for one customer, one account, one device — **give those records the same key**. They land in one partition and are ordered relative to each other. Records with different keys may be processed in any relative order, which is usually fine and is what allows parallelism.

Partition count is the **unit of parallelism**: a consumer group can have at most one consumer per partition doing useful work (Chapter 04). More partitions means more possible parallelism — and more open file handles, more replication traffic, longer leader-election times, and more metadata. Partitions can be **added** to a topic but not removed, and adding them **changes key-to-partition mapping** for future records, which breaks the ordering guarantee for existing keys. Choose deliberately.

## Replication, leaders, and the ISR

Each partition has a **replication factor**: one **leader** and some **followers** on other brokers. All reads and writes go to the leader; followers replicate.

The **ISR (in-sync replicas)** is the set of replicas currently caught up with the leader. It matters because:

- **`min.insync.replicas`** sets how many replicas must acknowledge a write when the producer uses `acks=all`.
- If the ISR shrinks below that minimum, the partition **stops accepting writes** rather than accepting data it cannot protect — availability is deliberately sacrificed for durability.
- Only ISR members are eligible to become leader (unless you enable unclean leader election, which trades data loss for availability).

The classic durable configuration is **replication factor 3 with `min.insync.replicas=2` and `acks=all`**: it survives one broker loss while still accepting writes, and refuses writes when two are gone.

## Retention

Kafka retains records by **time** (`retention.ms`) or **size** (`retention.bytes`), independent of whether anyone consumed them — a consumer can replay from any retained offset. Alternatively, **log compaction** retains the *latest* record per key indefinitely, turning a topic into a changelog of current state.

## Hands-On Lab

Python models the log. **Cost:** none.

### Lab 2.1 — Build a partitioned log with per-partition offsets

**Objective:** Show how keys map to partitions and where ordering holds.

```bash
python3 - <<'EOF'
NUM_PARTITIONS = 3
partitions = {p: [] for p in range(NUM_PARTITIONS)}

def produce(key, value):
    p = (hash(key) % NUM_PARTITIONS) if key is not None else len(sum(partitions.values(), [])) % NUM_PARTITIONS
    offset = len(partitions[p])
    partitions[p].append((offset, key, value))
    return p, offset

events = [("cust-1","created"),("cust-2","created"),("cust-1","updated"),
          ("cust-3","created"),("cust-1","deleted"),("cust-2","updated")]
for k, v in events:
    p, off = produce(k, v)
    print(f"key={k:7} value={v:8} -> partition {p}, offset {off}")

print()
for p, recs in partitions.items():
    print(f"partition {p}: {[(o,k,v) for o,k,v in recs]}")
print("\nAll cust-1 events share a partition, so their order (created->updated->deleted) is GUARANTEED.")
print("Order ACROSS partitions is not guaranteed — and does not need to be, since keys are independent.")
EOF
```

**Expected result:** Each key's events land consistently in one partition, so `cust-1`'s created → updated → deleted sequence is ordered, while events for different customers may interleave arbitrarily across partitions. This is the mental model to carry into every design decision: **key by the entity whose ordering matters.**

**Negative test:** Producing without a key when order matters — records round-robin across partitions, and `deleted` can be processed before `created` for the same customer, corrupting downstream state.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 2.2 — ISR, min.insync.replicas, and the durability trade

**Objective:** Model when a partition stops accepting writes.

```bash
python3 - <<'EOF'
def can_write(replication_factor, isr_size, min_isr, acks):
    if acks in (0, 1):
        return True, f"acks={acks}: leader alone accepts (fast, but data loss possible on leader failure)"
    if isr_size >= min_isr:
        return True, f"acks=all: ISR {isr_size} >= min.insync.replicas {min_isr} — durable write accepted"
    return False, (f"acks=all: ISR {isr_size} < min.insync.replicas {min_isr} — WRITES REJECTED "
                   f"(NotEnoughReplicas). Durability is preferred over availability by design")

print("Topic: RF=3, min.insync.replicas=2, producer acks=all\n")
for isr in (3, 2, 1):
    ok, why = can_write(3, isr, 2, "all")
    print(f"ISR size {isr}: {'WRITE OK ' if ok else 'REJECTED '} — {why}")
print()
ok, why = can_write(3, 1, 2, 1)
print(f"Same ISR=1 but acks=1: {'WRITE OK' if ok else 'REJECTED'} — {why}")
print("\nRF=3 + min.insync=2 + acks=all survives ONE broker loss and refuses writes at two.")
EOF
```

**Expected result:** Writes succeed with an ISR of 3 or 2 and are **rejected at 1** with `acks=all` — while the same situation with `acks=1` accepts the write and risks losing it. The rejection is not a malfunction: Kafka is choosing to stop rather than accept data it cannot replicate. Understanding that trade is the difference between panicking at a `NotEnoughReplicas` error and recognizing it as the system doing its job.

**Negative test:** Setting `min.insync.replicas` equal to the replication factor — you lose all fault tolerance for writes, because a single broker restart takes the partition offline for producers.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 2.3 — Choose partition count and understand the cost of change

**Objective:** Size partitions and see what repartitioning breaks.

```bash
python3 - <<'EOF'
def recommend_partitions(target_throughput_mbs, per_partition_mbs, max_consumers):
    by_throughput = -(-target_throughput_mbs // per_partition_mbs)
    return max(by_throughput, max_consumers), by_throughput

for throughput, per, consumers in [(100, 10, 6), (30, 10, 12), (500, 10, 8)]:
    rec, by_t = recommend_partitions(throughput, per, consumers)
    driver = "throughput" if by_t >= consumers else "consumer parallelism"
    print(f"target {throughput} MB/s, {per} MB/s per partition, {consumers} consumers -> {rec} partitions ({driver} drives it)")

print("\n--- what changing partition count breaks ---")
for np in (3, 4):
    mapping = {k: hash(k) % np for k in ("cust-1","cust-2","cust-3","cust-4")}
    print(f"{np} partitions: {mapping}")
print("\nAdding a partition REMAPS keys: future records for a key may land elsewhere, so ordering")
print("against that key's existing records is broken. Partitions can be added, never removed.")
EOF
```

**Expected result:** Partition count is driven by whichever is larger — throughput need or consumer parallelism — and the second half shows key-to-partition mapping **changing** when the count goes from 3 to 4. That remapping is why partition count is a decision to make deliberately up front: adding partitions later is easy mechanically and quietly breaks per-key ordering for existing keys.

**Negative test:** Over-provisioning to thousands of partitions "for headroom" — you pay in file handles, replication traffic, memory, and much slower leader election during broker failures, for parallelism no consumer group will ever use.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] The partitioned, append-only log and per-partition offsets modeled.
- [ ] Key-based partitioning used to obtain ordering where it matters.
- [ ] Replication, ISR, `min.insync.replicas`, and the durability-over-availability trade explained.
- [ ] Partition count sized deliberately, with the cost of later change understood.
