# Chapter 07: Associate DBA — Replication and Sharding

## Learning Objectives

- Explain replica sets, elections, and failover.
- Reason about write concern and read preference.
- Explain sharding and the role of the shard key.
- Choose a good shard key.
- Complete a walkthrough for each replication-and-sharding topic.

## Theory and Architecture

The **Associate DBA** validates MongoDB's high-availability and horizontal-scale architectures.
**Replication** uses a **replica set**: a group of `mongod` nodes holding the same data — one **primary**
(takes writes) and multiple **secondaries** (replicate the primary's **oplog**). If the primary fails,
the set holds an **election** and a secondary is promoted — automatic **failover**. **Write concern**
controls how many nodes must acknowledge a write (`w:1`, `w:"majority"`) before it returns, trading
durability for latency; **read preference** controls which nodes serve reads (`primary`,
`secondaryPreferred`, etc.). **Sharding** scales horizontally by partitioning a collection across
**shards** (each a replica set) using a **shard key**: MongoDB splits data into **chunks** by shard-key
range/hash, the **balancer** distributes chunks, and the **`mongos`** router directs queries using
**config servers** for metadata. The **shard key** choice is critical — it must have high **cardinality**,
low **frequency**, and match query patterns to avoid hotspots. This chapter teaches replication and
sharding with hands-on walkthroughs.

## Design Considerations

Run a **replica set** (odd number of voting members) for high availability; use **`w:"majority"`** for
durable writes and a suitable **read preference** for your latency/consistency needs. Shard only when a
single replica set cannot hold the data or throughput. Choose a **shard key** with high cardinality and
even distribution that supports your common queries — a **hashed** key spreads writes; a **ranged** key
supports range queries but risks hotspots on monotonically increasing values.

## Implementation and Automation

The labs read replica-set status, set write concern and read preference, and reason about shard-key
choice — the HA and scale skills the Associate DBA exam validates.

## Validation and Troubleshooting

Confirm replication and sharding:

```text
Replica set: primary (writes) + secondaries (replicate oplog); failure -> election -> failover
Write concern: w:1 (fast) vs w:"majority" (durable); Read preference: primary / secondaryPreferred / ...
Sharding: shard key -> chunks -> balancer distributes; mongos router + config servers
Shard key: high cardinality + low frequency + query-aligned; hashed spreads, ranged supports range
```

Common pitfalls: an even number of voting members (elections can tie); and a **low-cardinality** or
monotonically increasing **shard key** (creates hotspots/jumbo chunks).

## Security and Best Practices

Replication and sharding protect availability and scale of **your own** data. Secure the replica-set
keyfile/internal auth and the `mongos`/config servers. Choose write concern to avoid data loss on
failover. All work is authorized administration.

## Hands-On Lab

Replication-and-sharding walkthroughs. **Shared prerequisites** — a MongoDB replica set (or a single node
for the read-only checks), `mongosh`; `python3` for shard-key reasoning. **Cost:** none.

### Lab 7.1 — Read replica-set status

**Objective:** See the primary and secondaries.

```javascript
// mongosh (on a replica set)
rs.status().members.map(m => ({ name: m.name, state: m.stateStr }))
```

```text
[ { name: 'n1:27017', state: 'PRIMARY' },
  { name: 'n2:27017', state: 'SECONDARY' },
  { name: 'n3:27017', state: 'SECONDARY' } ]
```

**Expected result:** one PRIMARY and two SECONDARY members — a healthy 3-node replica set.

**Negative test:** run a 2-member set; an election can tie and fail to elect a primary — use an **odd**
number of voting members (or an arbiter).

**Cleanup:** none (read-only).

### Lab 7.2 — Set write concern for durability

**Objective:** Require majority acknowledgement.

```javascript
// mongosh
db.accounts.insertOne({ _id: 1, bal: 100 }, { writeConcern: { w: "majority", wtimeout: 5000 } })
```

```text
{ acknowledged: true, insertedId: 1 }
```

**Expected result:** the write returns only after a majority of nodes acknowledge — durable across
failover.

**Negative test:** write critical data with `w:1`; if the primary fails before replicating, the write can
be rolled back — use **`w:"majority"`** for durability.

**Cleanup:**

```javascript
// mongosh
db.accounts.drop()
```

### Lab 7.3 — Set a read preference

**Objective:** Route reads to secondaries where appropriate.

```javascript
// mongosh — read from a secondary for a reporting query
db.getMongo().setReadPref("secondaryPreferred")
db.orders.find({ status: "shipped" }).readPref("secondaryPreferred").count()
```

```text
2
```

**Expected result:** the reporting read served from a secondary — offloading the primary.

**Negative test:** send read-your-own-write queries to a secondary; replication lag can return stale data
— use `primary` for read-after-write.

**Cleanup:** none.

### Lab 7.4 — Choose a shard key

**Objective:** Evaluate shard-key candidates.

```python
python3 - <<'PY'
candidates = {
  "country":            "LOW cardinality -> few chunks, hotspots (BAD)",
  "createdAt (increasing)":"monotonic -> all writes hit one shard (BAD for writes)",
  "hashed(user_id)":    "high cardinality + even spread (GOOD for write scaling)",
  "{customer_id, order_date}":"compound, query-aligned + high cardinality (GOOD)",
}
for key, note in candidates.items():
    print(f"{key:26}: {note}")
print("Rule: shard key = high cardinality + low frequency + aligned to common queries")
PY
```

**Expected result:** each candidate judged — hashed user_id or a compound query-aligned key beats
low-cardinality or monotonic keys.

**Negative test:** shard on a monotonically increasing timestamp; every new write lands on the same shard
— use a **hashed** or high-cardinality compound key.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

MongoDB achieves high availability with replica sets (a primary and secondaries replicating the oplog,
with automatic elections and failover, tuned by write concern and read preference) and horizontal scale
with sharding (a collection partitioned by a well-chosen shard key into chunks the balancer distributes,
routed by `mongos`) — where the shard key must have high cardinality and match query patterns.

- [ ] I can read replica-set status and explain failover.
- [ ] I can set write concern and read preference.
- [ ] I can explain sharding, chunks, and the balancer.
- [ ] I can choose a good shard key.
- [ ] I completed Labs 7.1–7.4 including each negative test.
