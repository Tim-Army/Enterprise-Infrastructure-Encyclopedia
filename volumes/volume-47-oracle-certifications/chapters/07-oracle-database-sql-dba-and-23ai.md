# Chapter 07: Oracle Database — SQL, DBA, and 23ai

## Learning Objectives

- Explain the Oracle Database credentials: SQL Associate, DBA Associate/Professional.
- Summarize their exam topics.
- Apply SQL and core DBA skills (architecture, users, backup/recovery, multitenant).
- Understand Oracle Database 23ai and Autonomous Database.
- Complete a per-topic walkthrough for each Database area.

## Theory and Architecture

Oracle's database credentials span SQL through advanced administration:

- **Oracle Database SQL Certified Associate (1Z0-071)** — SQL: `SELECT`, DML, DDL,
  joins, subqueries, set operators, functions, constraints, and views.
- **Oracle Database Administration Associate (1Z0-082)** and **Professional
  (1Z0-083)** — database **architecture**, instance and storage management, **users
  and privileges**, **backup and recovery (RMAN)**, performance, and the
  **multitenant** architecture (**CDB/PDB**).
- **Oracle Database 23ai** — the current release ("ai"), adding **AI Vector
  Search**, **JSON Relational Duality**, and developer features; and **Autonomous
  Database** — the self-managing, self-securing, self-repairing DB.

## Design Considerations

**SQL** is the foundation for every data role. **DBA** adds operating the database:
the **CDB/PDB multitenant** model, storage (tablespaces, ASM), **RMAN** backup and
recovery, users/privileges/roles, and tuning. **23ai** modernizes the platform
(vector search for AI, JSON duality), and **Autonomous Database** offloads most DBA
toil. Practice on **Oracle Database Free** or **Autonomous Database (free tier)**.

## Implementation and Automation

The labs below use **real Oracle SQL** (runnable on Oracle Database Free/
Autonomous) and DBA concepts — SQL, joins/subqueries, DDL/constraints, multitenant,
RMAN, privileges, and 23ai vector search.

## Validation and Troubleshooting

Confirm the blueprints before studying:

```text
education.oracle.com > SQL Associate (1Z0-071) / DBA Associate (1Z0-082) / Professional (1Z0-083):
  - SQL: SELECT/DML/DDL, joins, subqueries, functions, constraints, views
  - DBA: architecture, multitenant (CDB/PDB), storage, users, backup/recovery (RMAN), tuning
  - target Database 23ai; practice on Oracle Database Free / Autonomous DB
```

Common pitfalls: MySQL/Postgres SQL dialect on Oracle (`FETCH FIRST`, `NVL`,
`DUAL`); ignoring the **multitenant** model (a PDB lives in a CDB); and confusing a
**role** with a **privilege**.

## Security and Best Practices

Grant least-privilege via **roles**; protect data with **RMAN** backups (test
restores); use the **multitenant** model to consolidate; and prefer **Autonomous
Database** where its automation fits. On 23ai, use **AI Vector Search** for
in-database RAG rather than exporting data.

## References and Knowledge Checks

- education.oracle.com: SQL and DBA exam topics; Oracle Database 23ai and Autonomous Database documentation.

**Knowledge checks**

1. What is the Oracle syntax to limit rows, and how does it differ from MySQL?
2. What is the CDB/PDB multitenant model?
3. What does Oracle Database 23ai AI Vector Search add?

## Hands-On Lab

Per-topic walkthroughs — SQL and DBA areas. SQL runs on Oracle Database Free /
Autonomous Database.

**Shared prerequisites** — access to Oracle Database Free or Autonomous Database
(free tier); `sqlplus`/SQL client. **Cost:** none (free tiers).

### Lab 7.1 — SQL: SELECT, filtering, and row limiting

**Objective:** Query with Oracle SQL syntax.

```sql
SELECT employee_id, last_name, salary
FROM   employees
WHERE  department_id = 60
ORDER  BY salary DESC
FETCH  FIRST 3 ROWS ONLY;
```

**Expected result:** the top-3 salaries in department 60 — core `SELECT`/`WHERE`/
`ORDER BY`/`FETCH FIRST` (Oracle row-limiting), the heart of 1Z0-071.

**Negative test:** use `LIMIT 3`; Oracle uses **`FETCH FIRST n ROWS ONLY`** — know
the dialect.

**Cleanup:** none.

### Lab 7.2 — SQL: joins and subqueries

**Objective:** Join tables and use a subquery.

```sql
SELECT e.last_name, d.department_name
FROM   employees e
JOIN   departments d ON e.department_id = d.department_id
WHERE  e.salary > (SELECT AVG(salary) FROM employees);
```

**Expected result:** employees earning above the average, with their department —
joins + a scalar subquery, key SQL Associate skills.

**Negative test:** join without an `ON`/`WHERE` condition (Cartesian product);
always specify the join predicate.

**Cleanup:** none.

### Lab 7.3 — SQL: DDL and constraints

**Objective:** Create a table with constraints.

```sql
CREATE TABLE projects (
  id        NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  name      VARCHAR2(100) NOT NULL,
  budget    NUMBER(12,2) CHECK (budget >= 0),
  owner_id  NUMBER REFERENCES employees(employee_id)
);
```

**Expected result:** a table with identity PK, NOT NULL, CHECK, and FK constraints
— the DDL/constraints area of 1Z0-071.

**Negative test:** enforce data rules only in the app; **constraints** enforce
integrity in the database — define them.

**Cleanup:** `DROP TABLE projects;`

### Lab 7.4 — DBA: multitenant (CDB/PDB)

**Objective:** Understand and inspect the multitenant model.

```sql
-- In a CDB:
SELECT name, open_mode FROM v$pdbs;      -- list pluggable databases
SHOW con_name;                            -- current container
ALTER SESSION SET CONTAINER = orclpdb1;   -- switch into a PDB
```

**Expected result:** the PDBs in the CDB and switching container — the multitenant
architecture central to the DBA exams.

**Negative test:** treat a PDB as a standalone instance; a **PDB** is a pluggable
database inside a **CDB** — understand the container model.

**Cleanup:** none.

### Lab 7.5 — DBA: users, privileges, and roles

**Objective:** Grant least-privilege access via a role.

```sql
CREATE ROLE app_read;
GRANT CREATE SESSION TO app_read;
GRANT SELECT ON hr.employees TO app_read;
CREATE USER analyst IDENTIFIED BY "S3cure#pw";
GRANT app_read TO analyst;
```

**Expected result:** a role granting only session + read, assigned to a user —
least-privilege access management (a DBA topic).

**Negative test:** `GRANT DBA TO analyst`; that is full privilege — grant a
**scoped role** instead.

**Cleanup:** `DROP USER analyst; DROP ROLE app_read;`

### Lab 7.6 — DBA: backup and recovery (RMAN)

**Objective:** Describe an RMAN backup strategy.

```bash
rman target /
# RMAN> BACKUP DATABASE PLUS ARCHIVELOG;      # full backup + redo
# RMAN> LIST BACKUP SUMMARY;                   # verify backups
# Recovery: RESTORE DATABASE; RECOVER DATABASE; -- to a point in time
```

**Expected result:** an RMAN backup-and-recovery workflow — the data-protection
area of the DBA exams.

**Negative test:** rely on OS file copies of an open database; use **RMAN** for
consistent, recoverable backups — and test restores.

**Cleanup:** none.

### Lab 7.7 — 23ai: AI Vector Search

**Objective:** Use native vector search in Oracle Database 23ai.

```sql
CREATE TABLE kb (id NUMBER, content CLOB, embedding VECTOR);
SELECT id, content
FROM   kb
ORDER  BY VECTOR_DISTANCE(embedding, :q, COSINE)
FETCH  FIRST 5 ROWS ONLY;
```

**Expected result:** a native vector-similarity query — the flagship 23ai feature
(AI Vector Search) enabling in-database RAG.

**Negative test:** export embeddings to a separate vector store when **23ai**
stores and searches vectors natively; keep them with the data where it fits.

**Cleanup:** `DROP TABLE kb;`

### Lab 7.8 — Autonomous Database

**Objective:** Describe what Autonomous Database automates.

```sql
-- Autonomous Database (ATP/ADW): self-driving, self-securing, self-repairing
-- Automates: provisioning, patching, tuning, backups, scaling (elastic OCPU/storage)
SELECT * FROM v$version;   -- still Oracle SQL; the DBA toil is automated away
```

**Expected result:** the Autonomous Database automation model — how it removes most
DBA toil while remaining Oracle SQL.

**Negative test:** hand-tune/patch an Autonomous Database; it **self-manages** —
focus on data and design, not maintenance.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The Oracle Database credentials span SQL (1Z0-071) through DBA Associate/
Professional (1Z0-082/083): querying, DDL/constraints, the CDB/PDB multitenant
model, users/roles, and RMAN backup/recovery — targeting **Database 23ai** (AI
Vector Search, JSON duality) and **Autonomous Database** (self-managing). SQL is
the foundation for every data role.

- [ ] I can write Oracle SQL (row limiting, joins, subqueries, DDL/constraints).
- [ ] I can navigate the CDB/PDB multitenant model.
- [ ] I can grant least-privilege roles and outline RMAN backup/recovery.
- [ ] I can use 23ai AI Vector Search and describe Autonomous Database.
- [ ] I completed Labs 7.1–7.8 including each negative test.
