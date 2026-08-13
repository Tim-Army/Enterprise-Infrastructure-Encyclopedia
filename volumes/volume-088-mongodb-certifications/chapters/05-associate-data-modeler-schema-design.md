# Chapter 05: Associate Data Modeler — Schema Design

## Learning Objectives

- Decide between embedding and referencing.
- Apply schema design patterns.
- Recognize schema anti-patterns.
- Respect the document size limit and cardinality.
- Complete a walkthrough for each schema-design topic.

## Theory and Architecture

The **Associate Data Modeler** validates designing document schemas for how applications actually access
data. The central decision is **embedding versus referencing**. **Embedding** nests related data in one
document — best when data is read together and has bounded size (one-to-few) — giving single-read access
and atomic updates. **Referencing** stores related data in separate documents linked by `_id` — best for
**one-to-many/large**, frequently-changing, or independently-accessed data, and unbounded growth.
Modeling is driven by **cardinality** (one-to-one, one-to-few, one-to-many, one-to-squillions) and the
application's **access patterns**. MongoDB documents an established set of **schema design patterns**
(subset, computed, bucket, extended reference, outlier) and **anti-patterns** (massive unbounded arrays,
bloated documents, too many collections). Every document is capped at **16 MB**, so unbounded embedding
is an anti-pattern. This chapter teaches schema design with hands-on `mongosh` walkthroughs.

## Design Considerations

Model to the **access pattern**: embed data read together and bounded; reference data that is large,
grows unbounded, or is accessed on its own. Use the **subset** pattern to embed the hot part and
reference the rest; the **computed** pattern to store precomputed aggregates; the **bucket** pattern for
time-series. Avoid **massive arrays** that grow without bound (approach the 16 MB limit and hurt
performance). Design for the queries, not for normalization.

## Implementation and Automation

The labs model an embedded document, a referenced relationship, and apply the subset pattern — the schema
design the Associate Data Modeler exam validates.

## Validation and Troubleshooting

Confirm schema design:

```text
Embed: read-together + bounded (one-to-few) -> single read, atomic update
Reference: large / unbounded / independently-accessed (one-to-many) -> linked by _id
Cardinality (one-to-few/many/squillions) + access pattern drive the choice
Patterns: subset, computed, bucket, extended reference, outlier
Anti-patterns: massive unbounded arrays, bloated docs, too many collections; 16MB doc limit
```

Common pitfalls: **embedding** an unbounded one-to-many (comments/events) that grows past limits —
**reference** it; and **referencing** small read-together data, forcing extra queries — **embed** it.

## Security and Best Practices

A schema shaped to access patterns is faster and simpler to secure (fewer joins, clearer ownership).
Model with least privilege in mind. All work is authorized design of your own data.

## Hands-On Lab

Schema-design walkthroughs. **Shared prerequisites** — a MongoDB instance with `mongosh`, `training`
database. **Cost:** none.

### Lab 5.1 — Embed read-together data

**Objective:** Model a bounded one-to-few relationship.

```javascript
// mongosh — a user with a few addresses (read together, bounded) => embed
db.users.insertOne({
  _id: "amy", name: "Amy",
  addresses: [ { type: "home", city: "Portland" }, { type: "work", city: "Seattle" } ]
})
db.users.findOne({ _id: "amy" }, { name: 1, "addresses.city": 1 })
```

```text
{ _id: 'amy', name: 'Amy', addresses: [ { city: 'Portland' }, { city: 'Seattle' } ] }
```

**Expected result:** the addresses embedded in the user — one read returns the user and addresses.

**Negative test:** put a user's two addresses in a separate `addresses` collection requiring a join on
every profile view; **embed** bounded read-together data.

**Rollback:** none yet.

### Lab 5.2 — Reference unbounded data

**Objective:** Model a one-to-many that grows.

```javascript
// mongosh — a user's orders grow unbounded => reference by user _id
db.userorders.insertMany([
  { _id: 101, user: "amy", total: 120 },
  { _id: 102, user: "amy", total: 300 }
])
db.userorders.find({ user: "amy" }).count()
```

```text
2
```

**Expected result:** orders stored separately and linked by `user` — the collection grows without
bloating the user document.

**Negative test:** embed every order in the user document; an active user's document grows toward the
**16 MB** limit — **reference** unbounded one-to-many data.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 5.3 — Apply the subset pattern

**Objective:** Embed the hot subset, reference the rest.

```javascript
// mongosh — product embeds its top reviews (subset); full reviews referenced
db.catalog.insertOne({
  _id: "p1", name: "Keyboard",
  top_reviews: [ { u: "amy", stars: 5 }, { u: "ben", stars: 4 } ],  // hot subset (embedded)
  reviews_count: 3120                                                // full set in `reviews` collection
})
db.catalog.findOne({ _id: "p1" }, { name: 1, top_reviews: 1, reviews_count: 1 })
```

```text
{ _id: 'p1', name: 'Keyboard', top_reviews: [ { u: 'amy', stars: 5 }, { u: 'ben', stars: 4 } ], reviews_count: 3120 }
```

**Expected result:** the product page reads the top reviews from one document; the full 3,120 reviews
live elsewhere — the subset pattern.

**Negative test:** embed all 3,120 reviews in the product; the document bloats and the page read slows —
embed a **subset**, reference the rest.

**Rollback:** none yet.

### Lab 5.4 — Apply the computed pattern

**Objective:** Store a precomputed aggregate instead of recomputing on every read.

```javascript
// mongosh — keep a running rating average on the product (computed pattern)
db.catalog.updateOne(
  { _id: "p1" },
  { $set: { rating_avg: 4.6, rating_count: 3120 } }   // maintained on each new review
)
db.catalog.findOne({ _id: "p1" }, { name: 1, rating_avg: 1, rating_count: 1 })
```

```text
{ _id: 'p1', name: 'Keyboard', rating_avg: 4.6, rating_count: 3120 }
```

**Expected result:** the product carries a precomputed rating average and count — the product page reads
it directly, no aggregation per view.

**Negative test:** run a `$group` aggregation over all 3,120 reviews on every product-page view; store
the **computed** average and update it on write instead.

**Rollback:**

```javascript
// mongosh
db.users.drop(); db.userorders.drop(); db.catalog.drop()
```

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The Associate Data Modeler shapes schemas to access patterns: embed bounded, read-together data
(one-to-few) for single-read access; reference large, unbounded, or independently-accessed data
(one-to-many) by `_id`; and apply patterns (subset, computed, bucket) while avoiding anti-patterns like
massive unbounded arrays that approach the 16 MB document limit.

- [ ] I can decide between embedding and referencing.
- [ ] I can reference an unbounded one-to-many relationship.
- [ ] I can apply the subset and computed patterns.
- [ ] I can recognize schema anti-patterns and the 16 MB limit.
- [ ] I completed Labs 5.1–5.4 including each negative test.
