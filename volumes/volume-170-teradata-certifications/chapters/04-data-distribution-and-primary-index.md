# Chapter 04: Data Distribution and the Primary Index

## Learning Objectives

- Explain how the Primary Index distributes rows across AMPs by hashing.
- Distinguish a good primary index (even distribution) from a skewed one.
- Understand access — how the primary index enables single-AMP retrieval.
- Recognize the primary index as the most important physical-design decision.

*Cert relevance: the Primary Index and data distribution are central to the Associate exam and Teradata design.*

## The Primary Index distributes data

The single most important concept in Teradata is the **Primary Index (PI)** — because it determines **how rows are distributed across the AMPs** ([Ch 3](03-the-mpp-architecture.md)). When you create a table, you choose a **primary index** (one or more columns). Teradata **hashes** the primary-index value of each row, and the hash decides **which AMP** the row lives on. This is not an "index" in the traditional sense (it is not a lookup structure on the side) — it is the **distribution mechanism**: the primary index **is** how the table's rows are spread across the parallel engine.

Because distribution drives parallelism, the primary index is the **foundation of performance**. Get it right and the AMPs are balanced and queries fly; get it wrong and you create skew that cripples the MPP advantage. Every Teradata table has a primary index (chosen or defaulted), and choosing it well is the designer's most consequential decision. The lab distributes rows by a primary index.

## Even distribution versus skew

The goal of a primary index is **even distribution** — each AMP holding roughly the **same number of rows** — so the parallel work is **balanced**:

- **Good primary index** — a column with **many distinct, evenly-spread values** (a unique or near-unique key like `order_id` or `customer_id`). Hashing spreads rows evenly across AMPs.
- **Bad primary index (skew)** — a column with **few distinct values** or a **dominant value** (like `country` where 80% are one value, or a column with many nulls). Hashing piles most rows onto a few AMPs, creating **skew** — some AMPs overloaded while others sit idle.

Skew is the enemy: as [Chapter 3](03-the-mpp-architecture.md) showed, a query waits for the **slowest (most loaded) AMP**, so a skewed table runs at the speed of its busiest AMP no matter how many AMPs exist. Choosing a **high-cardinality, evenly-distributed** column as the primary index is the core skill. The lab compares an even PI with a skewed one.

## Access by primary index

Beyond distribution, the primary index enables **fast access**:

- When you query **with an equality condition on the primary index** (`WHERE customer_id = 12345`), Teradata **hashes** the value and goes **directly to the single AMP** that holds that row — a **one-AMP operation**, extremely fast, touching only one processing unit.
- A **Unique Primary Index (UPI)** guarantees one row per value (fastest, no duplicates); a **Non-Unique Primary Index (NUPI)** allows duplicates (still single-AMP access, but multiple rows).
- Queries **not** using the primary index require **all-AMP** operations (every AMP scans its rows), which is fine for analytics but slower for single-row lookups.

So the primary index does double duty: **distribute rows evenly** (for parallel analytics) **and** provide **direct single-AMP access** (for point lookups). Balancing these is part of the design. The lab retrieves by primary index.

## The most important design decision

The primary index is the **most important physical-design decision** in Teradata, because it simultaneously governs:

- **Distribution** — even (good) or skewed (bad) across AMPs, driving parallel performance.
- **Access** — single-AMP retrieval when queried by the PI.
- **Join efficiency** — rows that share a primary index co-locate on the same AMPs, so joining on the PI is a **local, fast** operation (no redistribution over the BYNET, [Ch 5](05-sql-and-querying.md)).

Because it affects distribution, access, **and** joins, the primary index is where Teradata design **starts**, and it is heavily tested. A good rule: choose a primary index that is **high-cardinality (even distribution)**, **frequently used for access/joins**, and **stable**. The lab ties the three effects together. *(Distribution-by-key to co-locate joins is a general MPP/distributed-data principle.)*

## Hands-On Lab

Python models primary-index distribution, skew, single-AMP access, and join co-location. **Cost:** none.

### Lab 4.1 — Choose a primary index

**Objective:** Distribute by a good vs skewed PI, retrieve by PI, and co-locate a join.

```bash
python3 - <<'EOF'
N_AMPS = 8
def distribute(rows, pi_fn):
    amps = {i: [] for i in range(N_AMPS)}
    for r in rows: amps[hash(pi_fn(r)) % N_AMPS].append(r)
    return amps
def skew(amps):
    counts = [len(v) for v in amps.values()]
    return max(counts) / (sum(counts)/len(counts))   # max/avg; 1.0 = perfectly even

orders = [{"order_id": i, "country": "US" if i % 10 < 8 else ("DE" if i%10==8 else "FR")} for i in range(4000)]

# GOOD PI: order_id (high cardinality, unique) -> even
good = distribute(orders, lambda r: r["order_id"])
# BAD PI: country (low cardinality, 80% US) -> skew
bad  = distribute(orders, lambda r: r["country"])
print("PRIMARY INDEX distribution across 8 AMPs:")
print(f"   PI=order_id (UPI, high cardinality): per-AMP={[len(v) for v in good.values()]}  skew_factor={skew(good):.2f} (≈1 = even, GOOD)")
print(f"   PI=country  (low cardinality):       per-AMP={[len(v) for v in bad.values()]}  skew_factor={skew(bad):.2f} (>>1 = SKEW, BAD)")

# ACCESS by PI: WHERE order_id = X -> single AMP
x = 12345 % 4000
amp = hash(x) % N_AMPS
print(f"\nACCESS: WHERE order_id={x} -> hash -> AMP {amp} only (single-AMP, fast)")

# JOIN co-location: two tables with same PI co-locate -> local join (no BYNET redistribution)
print("\nJOIN: orders + order_items both PI=order_id -> matching rows on SAME AMP -> LOCAL join (fast, no redistribution)")
print()
print("The PRIMARY INDEX hashes rows to AMPs — it IS the distribution mechanism. A high-cardinality")
print("PI (order_id) spreads rows EVENLY (skew≈1); a low-cardinality one (country, 80% US) causes")
print("SKEW (one AMP overloaded). PI also gives single-AMP ACCESS (WHERE order_id=X) and co-locates")
print("JOINS on the same PI (local, no BYNET redistribution). It's the #1 Teradata design decision.")
EOF
```

**Expected result:** Rows distributed evenly by a high-cardinality primary index (order_id, skew ≈ 1) versus skewed by a low-cardinality one (country), single-AMP access by the primary index, and a co-located join on a shared primary index. The lesson is the Primary Index: it hashes rows to AMPs (the distribution mechanism), so a high-cardinality PI gives even distribution while a low-cardinality one causes skew, and the PI also enables single-AMP access and local joins — the most important Teradata design decision.

**Negative test:** Choosing a low-cardinality column (country, status) as the primary index. Most rows pile onto a few AMPs (skew), and queries run at the speed of the overloaded AMP; a high-cardinality, evenly-distributed primary index is what keeps the MPP engine balanced.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] The Primary Index understood — it hashes rows to AMPs and IS the distribution mechanism (not a side lookup).
- [ ] Even vs skew understood — high-cardinality PI distributes evenly; low-cardinality causes skew that cripples parallelism.
- [ ] Access understood — equality on the PI is a fast single-AMP operation (UPI/NUPI).
- [ ] The primary decision understood — the PI governs distribution, access, and join co-location together.

## See also

- [Chapter 03 — The MPP Architecture](03-the-mpp-architecture.md) — why even distribution across AMPs matters.
- [Chapter 05 — SQL and Querying at Scale](05-sql-and-querying.md) — joins and how the PI co-locates them.
- [Chapter 06 — Physical Database Design](06-physical-database-design.md) — other indexes and partitioning around the PI.
