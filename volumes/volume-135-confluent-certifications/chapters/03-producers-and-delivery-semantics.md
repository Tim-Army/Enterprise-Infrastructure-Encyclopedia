# Chapter 03: Producers and Delivery Semantics

## Learning Objectives

- Configure producer acknowledgements and understand what each level risks.
- Distinguish at-most-once, at-least-once, and exactly-once delivery.
- Use idempotent producers and transactions to achieve exactly-once semantics.
- Tune batching and compression without breaking ordering.

## Acknowledgements

The `acks` setting decides when a producer considers a write successful, and it is the central durability knob:

| `acks` | Producer waits for | Risk |
|:---|:---|:---|
| **0** | Nothing — fire and forget | Data lost silently if the broker never received it |
| **1** | Leader written | Lost if the leader fails before followers replicate |
| **all** (`-1`) | All in-sync replicas (per `min.insync.replicas`) | Slowest; safest |

`acks=all` with replication factor 3 and `min.insync.replicas=2` is the durable default from Chapter 02.

## Delivery semantics

| Semantic | Meaning | How you get it |
|:---|:---|:---|
| **At most once** | Records may be lost, never duplicated | `acks=0`/`1` with no retries |
| **At least once** | Records never lost, may be duplicated | `acks=all` with retries (the common default) |
| **Exactly once** | Neither lost nor duplicated | Idempotent producer + transactions |

**At-least-once produces duplicates for an unavoidable reason:** if a producer sends a record, the broker writes it, and the acknowledgement is lost in transit, the producer retries — and the broker now has two copies. The producer cannot tell a lost record from a lost acknowledgement.

## Idempotence and transactions

**Idempotent producer** (`enable.idempotence=true`) solves exactly that case. The producer is assigned a producer ID, and each record carries a sequence number; the broker deduplicates retries of the same sequence. It also implies `acks=all`, retries, and bounded in-flight requests. It is essentially free and should be on.

Idempotence deduplicates **per partition, per producer session**. For atomicity across multiple partitions or topics — the consume-process-produce pattern where you must commit input offsets and output records together — you need **transactions**: `initTransactions`, `beginTransaction`, produce and send offsets, then `commitTransaction` or `abortTransaction`. Consumers set `isolation.level=read_committed` to skip aborted records.

## Batching, compression, and ordering

Producers batch records per partition (`linger.ms` waits briefly to fill a batch; `batch.size` caps it). Batching plus compression (`lz4`, `zstd`, `snappy`, `gzip`) is where most producer throughput comes from — compression applies to the whole batch, so bigger batches compress better.

The ordering trap: `max.in.flight.requests.per.connection > 1` combined with **retries** can reorder records within a partition, because a retried batch may land after a later one. With **idempotence enabled**, Kafka preserves ordering for up to 5 in-flight requests — another reason to turn it on.

## Hands-On Lab

Python models producer semantics. **Cost:** none.

### Lab 3.1 — Acks and what each level loses

**Objective:** Model failure at each acknowledgement level.

```bash
python3 - <<'EOF'
def produce(acks, leader_fails_before_replication, broker_never_received):
    if broker_never_received:
        return ("LOST silently — producer never waited for confirmation" if acks == 0
                else "producer detects failure and can retry")
    if acks == 0:  return "written, but producer has no confirmation"
    if acks == 1:
        return ("LOST — leader acked then failed before followers replicated" if leader_fails_before_replication
                else "written and acked by leader")
    return "written and replicated to the in-sync replicas — durable"

print(f"{'acks':6}{'broker never got it':>24}{'leader dies after ack':>26}")
for acks in (0, 1, "all"):
    a = produce(acks, False, True)
    b = produce(acks, True, False)
    print(f"{str(acks):6}{a[:22]:>24}{b[:24]:>26}")
print("\nacks=0 loses data without telling you. acks=1 loses data on leader failure.")
print("acks=all + RF3 + min.insync=2 is the durable configuration.")
EOF
```

**Expected result:** `acks=0` loses records silently, `acks=1` loses them specifically when the leader dies between acknowledging and replicating, and `acks=all` survives both. The word "silently" is the important one — an `acks=0` pipeline can be losing data continuously with no error anywhere, which is why it belongs only where loss is genuinely acceptable (metrics samples, say, not orders).

**Negative test:** Choosing `acks=0` for throughput on a financial or ordering pipeline — the throughput gain is real and the data loss is invisible until reconciliation finds it.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 3.2 — Why at-least-once duplicates, and how idempotence fixes it

**Objective:** Reproduce the duplicate, then eliminate it.

```bash
python3 - <<'EOF'
log_plain, log_idem = [], []
seen_sequences = set()

def send_plain(record, ack_lost):
    log_plain.append(record)                       # broker writes it
    if ack_lost:
        log_plain.append(record)                   # producer retries -> DUPLICATE

def send_idempotent(record, seq, ack_lost):
    if seq not in seen_sequences:
        seen_sequences.add(seq); log_idem.append(record)
    if ack_lost:                                   # retry with the SAME sequence number
        if seq not in seen_sequences:
            log_idem.append(record)                # broker dedupes: no-op

for i, (rec, lost) in enumerate([("order-1", False), ("order-2", True), ("order-3", False)]):
    send_plain(rec, lost)
    send_idempotent(rec, i, lost)

print(f"plain producer      : {log_plain}   <- {len(log_plain)} records, order-2 DUPLICATED")
print(f"idempotent producer : {log_idem}   <- {len(log_idem)} records, exactly once per partition")
print("\nThe producer cannot distinguish 'record lost' from 'ack lost', so it must retry.")
print("Idempotence gives each record a sequence number so the broker can drop the retry.")
EOF
```

**Expected result:** The plain producer writes `order-2` twice because its acknowledgement was lost; the idempotent producer writes each record exactly once because the broker recognizes the retried sequence number. The explanation underneath is the part worth remembering: duplication is not a bug in at-least-once delivery, it is the **unavoidable consequence** of an unreliable acknowledgement path — and sequence numbers are what resolve it.

**Negative test:** Deduplicating in the consumer instead — workable but expensive, and it pushes correctness into every consumer rather than solving it once at the producer.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 3.3 — Transactions for consume-process-produce

**Objective:** Model atomic output plus offset commit.

```bash
python3 - <<'EOF'
class TxnProducer:
    def __init__(self): self.committed, self.pending, self.committed_offsets = [], [], {}
    def begin(self): self.pending = []
    def send(self, rec): self.pending.append(rec)
    def send_offsets(self, topic, offset): self._pending_offset = (topic, offset)
    def commit(self):
        self.committed += self.pending
        t, o = self._pending_offset; self.committed_offsets[t] = o
        self.pending = []; return "COMMIT — outputs and input offsets are atomic"
    def abort(self):
        dropped, self.pending = len(self.pending), []
        return f"ABORT — {dropped} pending record(s) discarded; input offset NOT advanced, so it reprocesses"

p = TxnProducer()
p.begin(); p.send("enriched-1"); p.send("enriched-2"); p.send_offsets("input", 42)
print(p.commit()); print(f"   committed={p.committed} offsets={p.committed_offsets}")

p.begin(); p.send("enriched-3"); p.send_offsets("input", 43)
print(p.abort()); print(f"   committed={p.committed} offsets={p.committed_offsets}")
print("\nConsumers with isolation.level=read_committed never see aborted records.")
print("Without transactions you could publish outputs and then fail before committing offsets,")
print("so reprocessing would publish them AGAIN — duplicates downstream.")
EOF
```

**Expected result:** The commit makes outputs and the input offset advance together; the abort discards outputs **and** leaves the offset where it was, so the input is safely reprocessed. The closing lines state the failure transactions prevent: without them, a crash between publishing outputs and committing offsets guarantees duplicates on restart. This consume-process-produce atomicity is what "exactly-once semantics" actually means in Kafka — not magic, but a transaction spanning outputs and offsets.

**Negative test:** Enabling transactions on the producer while consumers read with `isolation.level=read_uncommitted` — downstream consumers see aborted records, and the guarantee you paid for does not reach them.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] `acks` levels configured with their loss modes understood.
- [ ] At-most-once, at-least-once, and exactly-once distinguished.
- [ ] Idempotent producer used to eliminate retry duplicates per partition.
- [ ] Transactions applied to make outputs and offset commits atomic, with `read_committed` consumers.
- [ ] Batching, compression, and the in-flight/ordering interaction understood.
