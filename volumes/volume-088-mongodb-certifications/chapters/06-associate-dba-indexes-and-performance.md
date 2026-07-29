# Chapter 06: Associate DBA — Indexes and Performance

## Learning Objectives

- Create single-field and compound indexes.
- Read a query plan with `explain`.
- Apply the ESR rule for compound indexes.
- Reason about covered queries and index types.
- Complete a walkthrough for each index-and-performance topic.

## Theory and Architecture

The **Associate DBA** validates keeping MongoDB fast and healthy, and **indexes** are the core lever.
Without an index, a query does a **collection scan** (`COLLSCAN`) — reading every document. An index is a
B-tree on one or more fields that lets MongoDB find matching documents directly (`IXSCAN`). Types include
**single-field**, **compound** (multiple fields, order matters), **multikey** (over array fields),
**text** (search), and **geospatial**. The **`explain`** command shows the query plan — whether an index
was used, how many documents were examined versus returned, and the winning plan. For compound indexes,
the **ESR rule** orders fields as **Equality**, then **Sort**, then **Range** for best use. A **covered
query** is answered entirely from the index (all projected fields are in the index, `_id` excluded) — no
document fetch at all. This chapter teaches indexes and performance with hands-on `mongosh` walkthroughs.

## Design Considerations

Index the fields your queries **filter and sort** on, following the **ESR** order for compound indexes.
Aim for **covered queries** on hot read paths. Do not over-index — every index costs write performance
and storage. Use **`explain`** to confirm an `IXSCAN` (not `COLLSCAN`) and a low
`totalDocsExamined:nReturned` ratio. Add **text/geo** indexes for those query types.

## Implementation and Automation

The labs create indexes, read an `explain` plan, apply the ESR rule, and confirm a covered query — the
performance skills the Associate DBA exam validates.

## Validation and Troubleshooting

Confirm indexing and performance:

```text
No index -> COLLSCAN (reads every doc); index -> IXSCAN (direct lookup)
Types: single-field, compound (order matters), multikey (arrays), text, geospatial
explain(): winning plan + stage (IXSCAN/COLLSCAN) + docsExamined vs nReturned
ESR: compound index order = Equality, then Sort, then Range
Covered query: answered from the index alone (projected fields indexed, _id excluded) -> no fetch
```

Common pitfalls: a compound index in the wrong **ESR** order (a filter cannot use it well); and
over-indexing, slowing writes — index for real query patterns and verify with `explain`.

## Security and Best Practices

Well-indexed queries reduce load and denial-of-service risk from expensive scans. Grant index-management
rights only to DBAs. All work is authorized administration of your own database.

## Hands-On Lab

Index-and-performance walkthroughs. **Shared prerequisites** — a MongoDB instance with `mongosh`,
`training` database. **Cost:** none.

### Lab 6.1 — Create indexes and confirm an IXSCAN

**Objective:** Replace a collection scan with an index scan.

```javascript
// mongosh
for (let i = 0; i < 1000; i++) db.people.insertOne({ name: "u"+i, age: i % 90, city: "pdx" })
db.people.find({ age: 42 }).explain("executionStats").executionStats.totalDocsExamined   // before index
db.people.createIndex({ age: 1 })
db.people.find({ age: 42 }).explain("executionStats").executionStats.totalDocsExamined    // after index
```

```text
1000
12
```

**Expected result:** documents examined drops from 1000 (COLLSCAN) to ~matches (IXSCAN) after creating
the index.

**Negative test:** query `age` with no index on a large collection; it scans everything — create an
index.

**Cleanup:** none yet.

### Lab 6.2 — Read an explain plan

**Objective:** Confirm the winning plan uses the index.

```javascript
// mongosh
db.people.find({ age: 42 }).explain().queryPlanner.winningPlan.inputStage.stage
```

```text
IXSCAN
```

**Expected result:** the winning plan's stage is `IXSCAN` — the index is used.

**Negative test:** assume an index is used because it exists; a query on a different field still
`COLLSCAN`s — verify with **`explain`**.

**Cleanup:** none.

### Lab 6.3 — Apply the ESR rule

**Objective:** Order a compound index correctly.

```javascript
// mongosh — query: equality on city, sort by age, range on age
// ESR => Equality(city), Sort(age)  (age also serves the range)
db.people.createIndex({ city: 1, age: 1 })
db.people.find({ city: "pdx", age: { $gte: 40 } }).sort({ age: 1 })
        .explain().queryPlanner.winningPlan.inputStage.stage
```

```text
IXSCAN
```

**Expected result:** the `{city:1, age:1}` index (Equality then Sort/Range) serves the query with an
`IXSCAN` and no in-memory sort.

**Negative test:** build `{age:1, city:1}` for an equality-on-city query; the equality field should come
**first** — follow **ESR**.

**Cleanup:** none.

### Lab 6.4 — Confirm a covered query

**Objective:** Answer a query from the index alone.

```javascript
// mongosh — project only indexed fields, exclude _id -> covered
db.people.find({ city: "pdx", age: { $gte: 40 } }, { _id: 0, city: 1, age: 1 })
        .explain("executionStats").executionStats.totalDocsExamined
```

```text
0
```

**Expected result:** `totalDocsExamined: 0` — the query is answered entirely from the index (covered), no
document fetch.

**Negative test:** project a non-indexed field (e.g., `name`); MongoDB must fetch documents, so the query
is no longer covered — index (or omit) the projected fields.

**Cleanup:**

```javascript
// mongosh
db.people.drop()
```

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The Associate DBA keeps MongoDB fast with indexes: single-field, compound (ordered by the ESR rule —
Equality, Sort, Range), multikey, text, and geospatial — verified with `explain` to confirm an `IXSCAN`
and a low docs-examined ratio, and tuned toward covered queries answered from the index alone, without
over-indexing.

- [ ] I can create indexes and confirm an IXSCAN.
- [ ] I can read an explain plan.
- [ ] I can apply the ESR rule to a compound index.
- [ ] I can confirm a covered query.
- [ ] I completed Labs 6.1–6.4 including each negative test.
