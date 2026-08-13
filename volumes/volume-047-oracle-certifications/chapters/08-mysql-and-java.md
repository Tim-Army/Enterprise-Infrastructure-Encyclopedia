# Chapter 08: MySQL and Java

## Learning Objectives

- Explain the MySQL and Java certifications Oracle offers.
- Summarize their exam topics.
- Apply MySQL administration and development skills.
- Apply Java SE 21 language and API features.
- Complete a per-topic walkthrough for each MySQL and Java area.

## Theory and Architecture

Oracle stewards two of the most widely used technologies in software:

- **MySQL** — the world's most popular open-source database. Oracle certifies the
  **MySQL Database Administrator** (installation, configuration, security, backup,
  **replication**, **InnoDB**, and **HeatWave** analytics) and **MySQL Developer**
  (SQL and stored programs).
- **Java** — Oracle certifies the **Java SE Developer** at the current LTS release,
  **Java SE 21 (1Z0-830)**: the language and core APIs, including modern features
  like **records**, **sealed classes**, **pattern matching**, **virtual threads**,
  generics, collections, **streams/lambdas**, modules, and exception handling.

## Design Considerations

**MySQL** skills suit DBAs and developers working with the LAMP/open-source stack
and MySQL HeatWave on OCI. **Java SE 21** is the current professional Java target —
study the **new LTS features** (records, sealed types, pattern matching for
`switch`, virtual threads) alongside the enduring core (collections, streams,
generics, concurrency). Practice with a local **MySQL** and **JDK 21**.

## Implementation and Automation

The labs below use **real MySQL SQL/admin** and **Java SE 21** code you can run
locally, covering the core exam areas.

## Validation and Troubleshooting

Confirm the blueprints before studying:

```text
education.oracle.com > MySQL DBA/Developer and Java SE 21 Developer (1Z0-830):
  - MySQL: install/config, security, backup, replication, InnoDB, HeatWave; SQL + stored programs
  - Java SE 21: language + APIs incl. records, sealed classes, pattern matching, virtual threads
```

Common pitfalls: MyISAM vs **InnoDB** (use InnoDB for transactions);
`mysqldump` without a consistent snapshot; and studying **older Java** (11/17)
features when the exam targets **21**.

## Security and Best Practices

For MySQL: use **InnoDB** for ACID transactions, least-privilege users, TLS, and
tested **backups/replication**. For Java: prefer **immutable records**, **sealed**
hierarchies with exhaustive `switch` pattern matching, and **virtual threads** for
scalable concurrency; handle exceptions precisely and use the **Streams** API for
clear data processing.

## References and Knowledge Checks

- education.oracle.com: MySQL and Java SE 21 exam topics; dev.mysql.com; the Java SE 21 documentation.

**Knowledge checks**

1. Why use InnoDB over MyISAM for most MySQL workloads?
2. What are two Java SE 21 features new since Java 17?
3. What problem do Java virtual threads solve?

## Hands-On Lab

Per-topic walkthroughs — MySQL and Java areas. Run locally with MySQL and JDK 21.

**Shared prerequisites** — a local MySQL server and `mysql` client; **JDK 21**.
**Cost:** none.

### Lab 8.1 — MySQL: SQL and InnoDB transactions

**Objective:** Use a transaction on an InnoDB table.

```sql
CREATE TABLE accounts (id INT PRIMARY KEY, balance DECIMAL(12,2)) ENGINE=InnoDB;
INSERT INTO accounts VALUES (1, 100.00), (2, 0.00);
START TRANSACTION;
UPDATE accounts SET balance = balance - 50 WHERE id = 1;
UPDATE accounts SET balance = balance + 50 WHERE id = 2;
COMMIT;
SELECT * FROM accounts;
```

**Expected result:** a committed transfer (id 1 = 50, id 2 = 50) — ACID
transactions on **InnoDB**, a MySQL fundamental.

**Negative test:** run the transfer on a **MyISAM** table; it has no transactions,
so a mid-way failure leaves inconsistent data — use InnoDB.

**Rollback:** `DROP TABLE accounts;`

### Lab 8.2 — MySQL: users and privileges

**Objective:** Create a least-privilege MySQL user.

```sql
CREATE USER 'app'@'%' IDENTIFIED BY 'S3cure#pw';
GRANT SELECT, INSERT, UPDATE ON shop.* TO 'app'@'%';
FLUSH PRIVILEGES;
SHOW GRANTS FOR 'app'@'%';
```

**Expected result:** a user scoped to specific DML on one schema — least-privilege
access, a MySQL DBA skill.

**Negative test:** `GRANT ALL PRIVILEGES ON *.* ... WITH GRANT OPTION`; that is
superuser — scope to the schema and verbs needed.

**Rollback:** `DROP USER 'app'@'%';`

### Lab 8.3 — MySQL: backup and replication

**Objective:** Describe consistent backup and replication.

```bash
mysqldump --single-transaction --routines --triggers shop > shop.sql   # consistent backup (InnoDB)
# Replication: source (binlog) -> replica(s) via GTIDs for HA/read-scaling
```

**Expected result:** a consistent `mysqldump` and the replication model — the
backup/HA area of the MySQL DBA exam.

**Negative test:** `mysqldump` without `--single-transaction` on a busy InnoDB DB;
you risk an inconsistent snapshot — use it.

**Rollback:** `rm -f shop.sql`

### Lab 8.4 — Java SE 21: records and sealed classes

**Objective:** Model immutable data with records and sealed types.

```java
sealed interface Shape permits Circle, Square {}
record Circle(double r) implements Shape {}
record Square(double s) implements Shape {}
// records: immutable data carriers; sealed: a closed, exhaustive hierarchy
```

**Expected result:** an immutable `record` type and a `sealed` hierarchy — modern
Java SE 21 language features on the exam.

**Negative test:** write a verbose mutable class with manual getters/equals/
hashCode; a **record** generates them and is immutable — use it for data.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 8.5 — Java SE 21: pattern matching for switch

**Objective:** Use exhaustive pattern matching over a sealed type.

```java
double area(Shape s) {
    return switch (s) {
        case Circle c -> Math.PI * c.r() * c.r();
        case Square q -> q.s() * q.s();
    }; // no default needed: sealed + records make it exhaustive
}
```

**Expected result:** an exhaustive `switch` with type patterns — a flagship Java SE
21 feature.

**Negative test:** add an unreachable `default` and skip a permitted subtype; with
**sealed** types the compiler enforces exhaustiveness — rely on it.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 8.6 — Java SE 21: virtual threads

**Objective:** Use virtual threads for scalable concurrency.

```java
try (var executor = java.util.concurrent.Executors.newVirtualThreadPerTaskExecutor()) {
    for (int i = 0; i < 10_000; i++) {
        executor.submit(() -> { Thread.sleep(100); return 0; });
    }
} // 10k lightweight virtual threads — cheap blocking concurrency
```

**Expected result:** ten thousand virtual threads handling blocking work cheaply —
the Java 21 concurrency feature the exam covers.

**Negative test:** spawn 10,000 **platform** threads; that exhausts resources —
**virtual threads** make massive blocking concurrency cheap.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 8.7 — Java SE 21: streams and collections

**Objective:** Process data with the Streams API.

```java
import java.util.*; import java.util.stream.*;
var nums = List.of(3, 1, 4, 1, 5, 9, 2, 6);
var top3 = nums.stream().distinct().sorted(Comparator.reverseOrder())
               .limit(3).collect(Collectors.toList());
// top3 == [9, 6, 5]
```

**Expected result:** `[9, 6, 5]` via a stream pipeline (distinct → sort → limit) —
the collections/streams core of the Java exam.

**Negative test:** hand-write nested loops for this; the **Streams API** is clearer
and composable — use it for data processing.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Oracle certifies **MySQL** (DBA — InnoDB, users, backup, replication, HeatWave; and
Developer — SQL and stored programs) and **Java SE 21** (records, sealed classes,
pattern matching, virtual threads, streams, and the core APIs). Both are widely
used, practical credentials you can practice locally at no cost.

- [ ] I can use InnoDB transactions and least-privilege MySQL users.
- [ ] I can describe consistent MySQL backup and replication.
- [ ] I can use Java records, sealed types, and pattern matching.
- [ ] I can use virtual threads and the Streams API.
- [ ] I completed Labs 8.1–8.7 including each negative test.
