# Chapter 01: The MongoDB Certification Program

## Learning Objectives

- Describe the four MongoDB Associate certifications and what each validates.
- Explain the exam formats, ProctorU delivery, and Credly badges.
- Explain MongoDB University free training, Learning Paths, and discounts.
- Place the certifications against the document-database skill set.
- Complete a walkthrough for each program-orientation topic.

## Theory and Architecture

**MongoDB** certifications validate skills on the leading **document database** and its managed cloud
service, **Atlas**. MongoDB University offers four **Associate** certifications:

- **Associate Developer** — building modern applications with MongoDB and a driver (Node.js, Python,
  Java, PHP, or C#). Exam: **53 multiple-choice questions in 75 minutes**, online-proctored, **$150 USD**,
  no prerequisites.
- **Associate Database Administrator (DBA)** — building, supporting, and securing self-managed MongoDB
  infrastructure. Exam: **75 multiple-choice questions in 90 minutes**, online-proctored, **$150 USD**,
  no prerequisites.
- **Associate Atlas Administrator** — designing, operating, and managing deployments on **MongoDB
  Atlas**.
- **Associate Data Modeler** — data modeling for modern applications.

All exams are **online-proctored** (through **ProctorU**), multiple choice, offered in monthly exam
periods, and earn a **Credly** digital badge (with a listing in the Credly Talent Directory). Preparation
is built on **free MongoDB University** courses and **Learning Paths** — and completing a Learning Path
earns **50% off** the exam, while **students and educators** can earn a **free** exam through the student
and educator programs. This chapter orients you on a free MongoDB instance (Community locally, via
Docker, or a free Atlas M0 cluster) using `mongosh` so the certifications map to real commands.

## Design Considerations

Pick the certification that matches your role — **Developer** for application building, **Data Modeler**
for schema design, **DBA** for self-managed operations, **Atlas Administrator** for the managed cloud
service. Use the **free Learning Paths** to prepare and to earn the **50% discount** (or a free exam as a
student/educator). Because there are **no prerequisites**, you can start with any Associate exam, though
the document model and CRUD (Chapter 02) ground them all.

## Implementation and Automation

The labs connect to a MongoDB instance with `mongosh`, read the server version, and map the certification
ladder — the orientation every MongoDB candidate needs before the deeper chapters.

## Validation and Troubleshooting

Confirm the program map:

```text
Associate Developer   : build apps + drivers; 53 Q / 75 min; $150; online-proctored
Associate DBA         : self-managed build/support/secure; 75 Q / 90 min; $150
Associate Atlas Admin  : MongoDB Atlas (managed cloud) design/operate/manage
Associate Data Modeler : schema design / data modeling
Delivery: ProctorU online; Credly badges; monthly periods; no prereqs
Prep: free MongoDB University + Learning Paths; complete a path -> 50% off (students/educators free)
```

Common pitfalls: paying full price without completing a **Learning Path** (which earns 50% off); and
skipping the **document model/CRUD** foundation that every exam assumes.

## Security and Best Practices

MongoDB certifications validate building on and operating **your own** databases. Secure even your lab
instance (enable authentication early — Chapter 09). All work in this volume is authorized administration.

## Hands-On Lab

Program-orientation walkthroughs. **Shared prerequisites** — a free MongoDB instance (Community locally,
Docker, or a free Atlas M0 cluster) reachable with **`mongosh`**, and `python3` for ladder planning.
**Cost:** none (Community and Atlas M0 are free).

### Lab 1.1 — Connect and read the server version

**Objective:** Confirm the MongoDB version the exams assume.

```javascript
// mongosh
db.version()
db.hello().isWritablePrimary
```

```text
8.0.4
true
```

**Expected result:** the MongoDB server version and a writable primary — the platform the certifications
validate.

**Negative test:** study against a very old 4.x server; commands and the aggregation/`mongosh` surface
differ — practice on a current major version.

**Rollback:** none (read-only).

### Lab 1.2 — Map the certification ladder

**Objective:** Reason about the four Associate credentials.

```python
python3 - <<'PY'
certs = {
  "Associate Developer":     "build apps + drivers (53Q/75min, $150)",
  "Associate Data Modeler":  "schema design / data modeling",
  "Associate DBA":           "self-managed build/support/secure (75Q/90min, $150)",
  "Associate Atlas Admin":   "MongoDB Atlas managed cloud",
}
for cert, focus in certs.items():
    print(f"{cert:24}: {focus}")
print("No prereqs; the document model + CRUD grounds all four")
PY
```

**Expected result:** the four Associate certifications mapped to their focus and format.

**Negative test:** assume one MongoDB exam covers everything; there are **four** role-specific Associate
exams — pick the one for your role.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 1.3 — Confirm your database and readiness

**Objective:** See the database you will practice on.

```javascript
// mongosh
use training
db.getSiblingDB("training").runCommand({ ping: 1 })
db.getMongo().getDBNames()
```

```text
{ ok: 1 }
[ 'admin', 'config', 'local', 'training' ]
```

**Expected result:** a reachable `training` database (with the system databases) — a working practice
environment.

**Negative test:** practice against `admin` or `local`; use a dedicated `training` database so you do not
disturb system collections.

**Rollback:** none (read-only).

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

MongoDB University offers four Associate certifications — Developer, Data Modeler, Atlas Administrator,
and DBA — all online-proctored via ProctorU, multiple choice, $150 (Developer 53 Q/75 min; DBA 75 Q/90
min), with Credly badges, no prerequisites, and free University training whose Learning Paths earn a 50%
discount (or a free exam for students and educators).

- [ ] I can describe the four Associate certifications.
- [ ] I can explain the exam formats, ProctorU, and Credly badges.
- [ ] I can explain MongoDB University training and Learning Path discounts.
- [ ] I completed Labs 1.1–1.3 including each negative test.
