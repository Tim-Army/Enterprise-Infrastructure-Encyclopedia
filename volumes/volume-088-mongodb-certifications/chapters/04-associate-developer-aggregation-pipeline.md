# Chapter 04: Associate Developer — Aggregation Pipeline

## Learning Objectives

- Explain the aggregation pipeline model.
- Filter and group with `$match` and `$group`.
- Reshape with `$project` and `$unwind`.
- Join collections with `$lookup`.
- Complete a walkthrough for each aggregation topic.

## Theory and Architecture

The **aggregation pipeline** is MongoDB's framework for transforming and computing over documents. Data
flows through an ordered array of **stages**, each taking the previous stage's output — like a Unix pipe.
Key stages: **`$match`** (filter, like a query — put it first to reduce the working set), **`$group`**
(group by a key and compute **accumulators** such as `$sum`, `$avg`, `$max`, `$push`), **`$project`**
(include/exclude/compute fields), **`$sort`**, **`$limit`**, **`$unwind`** (expand an array into one
document per element), and **`$lookup`** (a left outer join to another collection). The pipeline is the
Associate Developer's tool for analytics, reporting, and reshaping — computing on the server, close to the
data, instead of pulling documents into the application. This chapter teaches the pipeline with hands-on
`mongosh` walkthroughs.

## Design Considerations

Put **`$match`** (and `$sort` on an indexed field) **early** so the pipeline processes fewer documents.
Use **`$group`** with the right accumulators for aggregates. Reshape with **`$project`** only what the
caller needs. Use **`$unwind`** before grouping array elements. Use **`$lookup`** for occasional joins,
but prefer an embedded model (Chapter 05) for data that is always read together. Watch pipeline memory
limits on large `$group`/`$sort` (allow disk use if needed).

## Implementation and Automation

The labs match and group, reshape and unwind, and join with `$lookup` — the aggregation the Associate
Developer exam validates.

## Validation and Troubleshooting

Confirm the pipeline:

```text
Pipeline = ordered stages; each feeds the next (like a Unix pipe)
$match (filter early) -> $group (key + accumulators $sum/$avg/$max/$push) -> $project (reshape)
$unwind (array -> one doc per element); $lookup (left outer join to another collection)
$sort/$limit; put $match + indexed $sort first to shrink the working set
```

Common pitfalls: `$match` placed **after** an expensive `$group`/`$lookup` (processes too much); and
`$lookup` on unindexed foreign fields (slow joins) — index the joined field.

## Security and Best Practices

Compute on the server with the pipeline instead of exporting raw data to the app. Scope aggregation to a
least-privilege read user. All work is authorized analytics on your own data.

## Hands-On Lab

Aggregation walkthroughs. **Shared prerequisites** — a MongoDB instance with `mongosh`, `training`
database. **Cost:** none.

### Lab 4.1 — Match and group

**Objective:** Aggregate revenue per customer.

```javascript
// mongosh
db.orders.insertMany([
  { cust: "amy", total: 120, status: "shipped" },
  { cust: "ben", total: 45,  status: "shipped" },
  { cust: "amy", total: 300, status: "shipped" },
  { cust: "amy", total: 60,  status: "cancelled" }
])
db.orders.aggregate([
  { $match: { status: "shipped" } },
  { $group: { _id: "$cust", revenue: { $sum: "$total" }, orders: { $sum: 1 } } },
  { $sort: { revenue: -1 } }
])
```

```text
[ { _id: 'amy', revenue: 420, orders: 2 }, { _id: 'ben', revenue: 45, orders: 1 } ]
```

**Expected result:** shipped-order revenue and count per customer, sorted — a match→group→sort pipeline.

**Negative test:** put `$match` after `$group`; the group processes cancelled orders too — filter
**first**.

**Rollback:** none yet.

### Lab 4.2 — Project computed fields

**Objective:** Reshape output.

```javascript
// mongosh
db.orders.aggregate([
  { $group: { _id: "$cust", revenue: { $sum: "$total" } } },
  { $project: { _id: 0, customer: "$_id", revenue: 1, tier: { $cond: [ { $gte: ["$revenue", 300] }, "gold", "standard" ] } } }
])
```

```text
[ { revenue: 480, customer: 'amy', tier: 'gold' }, { revenue: 45, customer: 'ben', tier: 'standard' } ]
```

**Expected result:** a reshaped result with a computed `tier` field — `$project` transforms the output.

**Negative test:** return the raw grouped docs and compute the tier in the app; compute it in
**`$project`** on the server.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 4.3 — Unwind an array

**Objective:** Expand array elements for grouping.

```javascript
// mongosh
db.carts.insertOne({ cust: "amy", items: ["a","b","a"] })
db.carts.aggregate([
  { $unwind: "$items" },
  { $group: { _id: "$items", count: { $sum: 1 } } },
  { $sort: { count: -1 } }
])
```

```text
[ { _id: 'a', count: 2 }, { _id: 'b', count: 1 } ]
```

**Expected result:** each array element counted after `$unwind` — array analytics.

**Negative test:** `$group` on the array field directly; you group by the whole array, not its elements —
`$unwind` first.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 4.4 — Join with `$lookup`

**Objective:** Enrich orders with customer data.

```javascript
// mongosh
db.customers.insertMany([{ _id: "amy", region: "west" }, { _id: "ben", region: "east" }])
db.orders.aggregate([
  { $group: { _id: "$cust", revenue: { $sum: "$total" } } },
  { $lookup: { from: "customers", localField: "_id", foreignField: "_id", as: "c" } },
  { $project: { _id: 0, cust: "$_id", revenue: 1, region: { $first: "$c.region" } } }
])
```

```text
[ { revenue: 480, cust: 'amy', region: 'west' }, { revenue: 45, cust: 'ben', region: 'east' } ]
```

**Expected result:** each customer's revenue enriched with their region via `$lookup` — a server-side
join.

**Negative test:** fetch orders and customers separately and join in the app; use **`$lookup`** for an
occasional join (or embed if always read together).

**Rollback:**

```javascript
// mongosh
db.orders.drop(); db.carts.drop(); db.customers.drop()
```

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The aggregation pipeline transforms documents through ordered stages: `$match` filters early, `$group`
computes accumulators, `$project` reshapes, `$unwind` expands arrays, and `$lookup` joins collections —
computing on the server instead of pulling data into the application, with `$match` and indexed `$sort`
placed first for efficiency.

- [ ] I can build a match→group→sort pipeline.
- [ ] I can project computed fields.
- [ ] I can unwind an array for grouping.
- [ ] I can join collections with `$lookup`.
- [ ] I completed Labs 4.1–4.4 including each negative test.
