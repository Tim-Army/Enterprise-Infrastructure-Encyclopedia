# Chapter 01: The Oracle Certification Program

## Learning Objectives

- Explain what Oracle certifies across its four families (OCI, Database, MySQL, Java).
- Describe the credential tiers and the year-versioned exam-code system.
- Explain the exam experience (Pearson VUE), exam topics, and Oracle CertView.
- Understand recent additions (OCI Generative AI, Multicloud, Database 23ai, Java 21).
- Verify a current exam and its topics from the authoritative source.

## Theory and Architecture

**Oracle** runs one of the industry's largest certification programs, spanning four
families: **Oracle Cloud Infrastructure (OCI)**, **Oracle Database**, **MySQL**,
and **Java**. Its footprint is enormous — Oracle Database and Java are foundational
to countless enterprises, and OCI is a major cloud — so this volume adds a large,
previously uncovered vendor to the encyclopedia alongside the other cloud (AWS,
Azure, Google Cloud) and data volumes.

The program is organized by family and tier:

- **OCI** — Foundations and AI Foundations (Associate), Architect (Associate and
  Professional), Developer, Operations, DevOps, Networking, Security, Multicloud,
  Data Science, and **Generative AI Professional**.
- **Oracle Database** — SQL (Associate), Database Administration (Associate and
  Professional), the current **Database 23ai** release, and Autonomous Database.
- **MySQL** — Database Administrator and Developer.
- **Java** — Java SE Developer (currently **Java SE 21**, the LTS release).

Oracle uses **year-versioned exam codes** — for example, OCI Foundations
**1Z0-1085-25**, OCI Architect Associate **1Z0-1072-26**, OCI Generative AI
Professional **1Z0-1127-26** — that roll forward annually as the exams refresh.

## Design Considerations

Choose a path by **family and role**. Cloud practitioners start with **OCI
Foundations** and branch to Architect, Developer, or a specialty (Networking,
Security, Data Science, **Generative AI**). Database professionals take **SQL →
DBA**, targeting **Database 23ai** (the "AI" release with AI Vector Search). Java
developers take **Java SE 21**, and data teams add **MySQL**. Because codes are
**year-versioned**, always confirm the **current suffix** — a "-24" course targets
a superseded exam.

## Implementation and Automation

Oracle publishes **exam topics** (sections) per exam — the authoritative study
scope — on each certification page, and manages credentials in **Oracle CertView**.
The labs in this volume use **SQL** (runnable on Oracle Database, including the
free Autonomous Database and Oracle Database Free), the **OCI CLI** (`oci`,
illustrative), **MySQL**, and **Java**:

```bash
# Confirm the tooling the exams exercise
sqlplus -v 2>/dev/null || echo "(Oracle SQL: use Oracle DB Free / Autonomous DB free tier)"
oci --version 2>/dev/null || echo "(OCI CLI for cloud labs)"
java -version 2>&1 | head -1 || echo "(JDK 21 for Java SE 21)"
```

## Validation and Troubleshooting

Confirm a credential's exam and topics on its certification page:

```text
education.oracle.com > Certifications > open the certification:
  - the current exam code (with year suffix) and exam topics (sections)
  - number of questions, duration, and passing score
  - recommended courses and hands-on practice
```

Common pitfalls: studying a **prior-year** exam version (check the suffix);
confusing **OCI Architect Associate vs Professional** scope; and assuming Oracle
Database and MySQL certs overlap (they are separate products/exams).

## Security and Best Practices

Verify facts on **education.oracle.com**, never a dump site. Practice on **free
tiers** — the OCI Always Free tier, **Oracle Database Free**/Autonomous Database,
and **MySQL** — so labs cost nothing. Track the **year-versioned** code so you
study the current exam, and manage credentials in **CertView**.

## References and Knowledge Checks

- education.oracle.com: the certification catalog, per-exam topics, and Oracle CertView; Oracle Learning Explorer (free training).

**Knowledge checks**

1. What are Oracle's four certification families?
2. What does the year suffix in an Oracle exam code signify?
3. What is Oracle Database 23ai, and why is it notable?

## Hands-On Lab

Exam-preparation walkthroughs for reading the program and confirming tooling.

**Shared prerequisites for Labs 1.1–1.3** — a shell with `curl`; access to a free
Oracle tier (Autonomous Database / Oracle Database Free) for SQL. **Cost:** none
(free tiers).

### Lab 1.1 — Enumerate the certification families (Topic: Read the program)

**Objective:** Identify the families and a current exam code.

```bash
curl -sSL -A "Mozilla/5.0" "https://education.oracle.com/certification" \
  | grep -oiE '1Z0-[0-9]{3,4}(-[0-9]{2})?' | sort -u | head
```

**Expected result:** current `1Z0-####` exam codes (many year-versioned, e.g.,
`-25`/`-26`) across OCI, Database, MySQL, and Java — the program's breadth.

**Negative test:** rely on a fixed code with no year suffix for OCI; the **suffix
rolls annually** — confirm the current one.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 1.2 — Confirm the tooling (Topic: Prepare to practice)

**Objective:** Verify the CLIs/runtimes the exams exercise.

```bash
sqlplus -v 2>/dev/null || echo "SQL: use Oracle Database Free or Autonomous DB (free)"
java -version 2>&1 | head -1 || echo "JDK: install JDK 21 for Java SE 21"
```

**Expected result:** SQL and Java tooling present (or the free-tier pointers) — the
practice environment for Oracle labs.

**Negative test:** study Java SE 21 on an old JDK; language features differ by
version — use **JDK 21**.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 1.3 — Run your first SQL (Topic: SQL foundation)

**Objective:** Confirm the SQL foundation Database certs build on.

```sql
SELECT table_name FROM user_tables ORDER BY table_name FETCH FIRST 5 ROWS ONLY;
```

**Expected result (on Oracle DB):** up to five of your schema's tables — basic SQL
(`SELECT`, `ORDER BY`, `FETCH FIRST`) that the SQL Associate exam certifies.

**Negative test:** use `LIMIT 5` (MySQL/Postgres syntax) on Oracle; Oracle uses
**`FETCH FIRST n ROWS ONLY`** — know the dialect.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Oracle certifies across four families — OCI (cloud), Oracle Database, MySQL, and
Java — with year-versioned exam codes that refresh annually. The program spans
foundations to professional specialties, including the new OCI Generative AI
Professional, Multicloud Architect, Database 23ai, and Java SE 21. Practice on
Oracle's free tiers and confirm the current exam code before studying.

- [ ] I can name Oracle's four certification families.
- [ ] I can explain the year-versioned exam-code system.
- [ ] I can confirm tooling and run basic Oracle SQL.
- [ ] I can find current exam topics on education.oracle.com.
- [ ] I completed Labs 1.1–1.3 including each negative test.
