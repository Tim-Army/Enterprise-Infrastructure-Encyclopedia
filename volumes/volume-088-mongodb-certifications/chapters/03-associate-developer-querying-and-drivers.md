# Chapter 03: Associate Developer — Querying and Drivers

## Learning Objectives

- Query with comparison, logical, and array operators.
- Shape results with projection, sort, limit, and skip.
- Reason about cursors.
- Connect from a driver (Node.js/Python/Java).
- Complete a walkthrough for each querying-and-drivers topic.

## Theory and Architecture

The **Associate Developer** exam validates building applications with MongoDB and a **driver**. Querying
uses a rich set of operators inside the `find` filter: **comparison** (`$eq`, `$gt`, `$gte`, `$lt`,
`$in`, `$ne`), **logical** (`$and`, `$or`, `$not`), **element** (`$exists`, `$type`), and **array**
(`$all`, `$elemMatch`, `$size`). Results are shaped with **projection** (include/exclude fields), and
**cursor** methods **`sort`**, **`limit`**, and **`skip`**. A **cursor** is a pointer to the result set
that the driver iterates lazily, fetching batches — important for large results. Applications talk to
MongoDB through official **drivers** (Node.js, Python/PyMongo, Java, PHP, C#), which expose the same
query and CRUD API in each language, manage the connection pool, and return language-native objects.
This chapter teaches developer querying and driver use with hands-on walkthroughs (`mongosh` plus
representative driver code).

## Design Considerations

Write **selective** query filters (matched by indexes, Chapter 06) and **project** only needed fields to
cut network and memory. Use **`sort`/`limit`** for top-N queries and **`skip`** sparingly (it scans
skipped documents — prefer range queries for pagination). From a **driver**, reuse a single client
(connection pool) rather than connecting per request, and handle cursors so they are exhausted or closed.

## Implementation and Automation

The labs query with operators, shape results with projection and cursor methods, and connect from a
driver — the developer skills the Associate Developer exam validates.

## Validation and Troubleshooting

Confirm developer querying:

```text
Operators: comparison ($gt/$in/$ne) + logical ($and/$or) + element ($exists) + array ($elemMatch/$all)
Shape: projection (fields) + sort + limit + skip (cursor methods)
Cursor = lazy pointer to results, iterated in batches by the driver
Drivers: Node/PyMongo/Java/PHP/C# — same API, connection pool, native objects; reuse one client
```

Common pitfalls: paginating deep result sets with **`skip`** (slow — it scans skipped docs); and opening
a new driver **client per request** (exhausts connections) instead of reusing one.

## Security and Best Practices

Build query filters from validated input (never interpolate untrusted data into a query), project
minimally, and connect with a least-privilege database user. All work is authorized application
development against your own database.

## Hands-On Lab

Querying-and-drivers walkthroughs. **Shared prerequisites** — a MongoDB instance with `mongosh`, the
`training` database, and (optionally) a driver runtime (Node/Python). **Cost:** none.

### Lab 3.1 — Query with operators

**Objective:** Filter with comparison and array operators.

```javascript
// mongosh
db.orders.insertMany([
  { _id: 1, cust: "amy", total: 120, items: ["a","b"], status: "shipped" },
  { _id: 2, cust: "ben", total: 45,  items: ["a"],     status: "pending" },
  { _id: 3, cust: "amy", total: 300, items: ["c","d"], status: "shipped" }
])
db.orders.find({ total: { $gte: 100 }, status: { $in: ["shipped","paid"] } }, { cust: 1, total: 1, _id: 0 })
```

```text
[ { cust: 'amy', total: 120 }, { cust: 'amy', total: 300 } ]
```

**Expected result:** orders of at least 100 with a shipped/paid status — a compound operator query.

**Negative test:** filter `items == "a"` with `{ items: { $eq: ["a"] } }` expecting element match; that
matches the whole array — query array membership with `{ items: "a" }` or `$elemMatch`.

**Rollback:** none yet.

### Lab 3.2 — Sort, limit, and project

**Objective:** Return a shaped top-N.

```javascript
// mongosh
db.orders.find({ status: "shipped" }, { cust: 1, total: 1, _id: 0 }).sort({ total: -1 }).limit(2)
```

```text
[ { cust: 'amy', total: 300 }, { cust: 'amy', total: 120 } ]
```

**Expected result:** the two highest-value shipped orders, projected — a shaped result set.

**Negative test:** fetch all documents into the app and sort in code; push **`sort`/`limit`** to the
server (ideally index-backed) instead.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 3.3 — Paginate correctly

**Objective:** Page results without deep `skip`.

```javascript
// mongosh
// page 2 by range (last seen _id = 1), not skip
db.orders.find({ _id: { $gt: 1 } }).sort({ _id: 1 }).limit(2)
```

```text
[ { _id: 2, cust: 'ben', ... }, { _id: 3, cust: 'amy', ... } ]
```

**Expected result:** the next page fetched by a range on `_id` — efficient, no skipped-document scan.

**Negative test:** page 10,000 with `.skip(20000).limit(2)`; MongoDB scans 20,000 documents first — use a
**range** on an indexed field.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 3.4 — Connect from a driver

**Objective:** Run the same query from application code.

```python
# Python / PyMongo (reuse one client for the app)
from pymongo import MongoClient
client = MongoClient("mongodb://localhost:27017")
db = client["training"]
top = list(db.orders.find({"status": "shipped"}, {"cust": 1, "total": 1, "_id": 0})
                    .sort("total", -1).limit(2))
print(top)   # [{'cust': 'amy', 'total': 300}, {'cust': 'amy', 'total': 120}]
```

**Expected result:** the driver returns the same shaped results as `mongosh`, as native Python dicts.

**Negative test:** create a `MongoClient` inside every request handler; reuse **one** client
(connection pool) for the process.

**Rollback:**

```javascript
// mongosh
db.orders.drop()
```

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The Associate Developer queries with comparison, logical, element, and array operators; shapes results
with projection, sort, limit, and skip over lazily iterated cursors; and connects through official
drivers (Node.js, Python, Java, PHP, C#) that share one query API and a reused connection pool — avoiding
deep `skip` pagination and per-request clients.

- [ ] I can query with operators.
- [ ] I can shape results with projection, sort, and limit.
- [ ] I can paginate with a range instead of deep skip.
- [ ] I can connect and query from a driver.
- [ ] I completed Labs 3.1–3.4 including each negative test.
