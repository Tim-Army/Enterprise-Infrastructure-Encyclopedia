# Chapter 02: The Document Model and CRUD

## Learning Objectives

- Explain the document model (BSON documents, collections, databases).
- Insert documents into a collection.
- Read documents with `find` and query filters.
- Update and delete documents.
- Complete a walkthrough for each document-and-CRUD topic.

## Theory and Architecture

MongoDB stores data as **documents** — field-and-value structures serialized as **BSON** (Binary JSON),
which extends JSON with types like `ObjectId`, `Date`, `Decimal128`, and binary data. Documents live in
**collections** (analogous to tables but schema-flexible: documents in one collection may differ), and
collections live in **databases**. Every document has a unique **`_id`** (an `ObjectId` by default). The
document model lets related data live **together** in one document (embedding), which often replaces the
joins a relational model needs. The core operations are **CRUD**: **create** (`insertOne`/`insertMany`),
**read** (`find`/`findOne` with query filters), **update** (`updateOne`/`updateMany` with update
operators like `$set`, `$inc`, `$push`), and **delete** (`deleteOne`/`deleteMany`). This chapter — the
foundation every MongoDB certification assumes — teaches the document model and CRUD with hands-on
`mongosh` walkthroughs.

## Design Considerations

Model data as **documents** shaped for how the application reads it — embed related data that is read
together. Give documents a meaningful **`_id`** where natural, or accept the default `ObjectId`. Use
**`insertMany`** for bulk loads, targeted **query filters** for reads, **update operators** (not
whole-document replacement) to change fields, and the precise **`deleteOne`/`deleteMany`** to remove
data. Respect the **16 MB** document size limit (Chapter 05).

## Implementation and Automation

The labs insert, read, update, and delete documents in a collection — the CRUD foundation the Developer,
Data Modeler, and DBA exams all build on.

## Validation and Troubleshooting

Confirm the document model and CRUD:

```text
BSON document (fields + typed values, _id) -> collection (schema-flexible) -> database
Create: insertOne / insertMany     Read: find / findOne (+ query filter)
Update: updateOne / updateMany (+ $set/$inc/$push)   Delete: deleteOne / deleteMany
Embedding keeps related data together (often replaces joins)
```

Common pitfalls: replacing a whole document when you meant to change one field (use **`$set`**); and
`updateMany`/`deleteMany` with an empty filter, which hits **every** document — filter precisely.

## Security and Best Practices

Use precise filters on updates and deletes, and least-privilege database users (Chapter 09). Validate
input in the application. All work is authorized administration of your own database.

## Hands-On Lab

Document-and-CRUD walkthroughs. **Shared prerequisites** — a MongoDB instance with `mongosh`, using the
`training` database. **Cost:** none.

### Lab 2.1 — Insert documents

**Objective:** Create documents in a collection.

```javascript
// mongosh
use training
db.products.insertMany([
  { _id: 1, name: "Keyboard", price: 45, tags: ["input","usb"] },
  { _id: 2, name: "Monitor",  price: 210, tags: ["display"] },
  { _id: 3, name: "Mouse",    price: 25, tags: ["input","usb"] }
])
```

```text
{ acknowledged: true, insertedIds: { '0': 1, '1': 2, '2': 3 } }
```

**Expected result:** three documents inserted into `products` — a schema-flexible collection.

**Negative test:** insert two documents with the same `_id: 1`; the second is rejected as a duplicate
key — `_id` is unique.

**Rollback:** none yet (used by later labs).

### Lab 2.2 — Read with a query filter

**Objective:** Find matching documents.

```javascript
// mongosh
db.products.find({ tags: "input" }, { name: 1, price: 1, _id: 0 })
```

```text
[ { name: 'Keyboard', price: 45 }, { name: 'Mouse', price: 25 } ]
```

**Expected result:** only the input devices, projected to `name` and `price` — a filtered, projected
read.

**Negative test:** run `find({})` on a huge collection and scroll everything; add a **query filter** and
projection to fetch only what you need.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 2.3 — Update with operators

**Objective:** Change fields without replacing the document.

```javascript
// mongosh
db.products.updateOne({ _id: 1 }, { $set: { price: 40 }, $push: { tags: "sale" } })
db.products.findOne({ _id: 1 })
```

```text
{ _id: 1, name: 'Keyboard', price: 40, tags: [ 'input', 'usb', 'sale' ] }
```

**Expected result:** the price updated and a tag pushed — a targeted field update, not a replacement.

**Negative test:** `updateOne({_id:1}, {price:40})` without `$set`; that **replaces** the whole document
(losing `name`/`tags`) — always use update operators.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 2.4 — Delete precisely

**Objective:** Remove only intended documents.

```javascript
// mongosh
db.products.deleteOne({ _id: 3 })
db.products.countDocuments()
```

```text
{ acknowledged: true, deletedCount: 1 }
2
```

**Expected result:** exactly one document removed, two remaining — a precise delete.

**Negative test:** `deleteMany({})`; that empties the whole collection — always pass a filter.

**Rollback:**

```javascript
// mongosh
db.products.drop()
```

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

MongoDB stores schema-flexible BSON documents in collections within databases, each with a unique `_id`,
and related data is often embedded to replace joins. CRUD is insertOne/insertMany, find/findOne with
query filters and projection, updateOne/updateMany with operators like `$set`, and deleteOne/deleteMany
with precise filters — the foundation every MongoDB exam assumes.

- [ ] I can explain the document model (BSON, collections, databases).
- [ ] I can insert documents.
- [ ] I can read with query filters and projection.
- [ ] I can update with operators and delete precisely.
- [ ] I completed Labs 2.1–2.4 including each negative test.
