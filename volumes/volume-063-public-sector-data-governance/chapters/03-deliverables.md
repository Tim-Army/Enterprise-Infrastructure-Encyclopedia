# Chapter 03: Public Sector Data Governance Deliverables

## Learning Objectives

- Identify the core deliverables of a public-sector data governance program.
- Author a data governance charter and a data policy.
- Build a data catalog/inventory entry with public-sector metadata.
- Construct a data-quality framework and scorecard.
- Complete a walkthrough for each Deliverables sub-topic.

## Theory and Architecture

**Deliverables** are the concrete, durable artifacts a governance program produces — the
"what." The exam expects fluency in five: (1) a **governance charter** — the founding document
that states scope, authority, drivers, and governing bodies; (2) **policies and standards** —
enforceable rules (data classification, quality, retention, access) with owners and review
cycles; (3) a **data catalog / inventory** with **metadata** — an authoritative register of
datasets, their owners, classifications, and lineage (in government, often feeding a public
open-data inventory); (4) a **data-quality framework and scorecard** — measurable dimensions
(completeness, accuracy, timeliness, consistency, validity, uniqueness) with thresholds; and
(5) **stewardship operating-model artifacts** — the workflows and RACI that make the above
run. Deliverables are how drivers become operational and how compliance becomes auditable.

## Design Considerations

Sequence deliverables: **charter first** (authority), then **policies** (rules), then
**catalog and quality** (execution and measurement). Keep every deliverable **owned**,
**dated**, and **reviewed** on a cycle. Prefer machine-readable artifacts (a catalog as
data, a scorecard as a query) so they can be audited and automated.

## Implementation and Automation

The labs author a charter, a policy, a catalog entry, a data-quality scorecard (SQL), and a
deliverables register.

## Validation and Troubleshooting

Confirm the deliverable set:

```text
Deliverables: (1) charter; (2) policies & standards; (3) catalog/inventory + metadata;
(4) data-quality framework + scorecard; (5) stewardship operating-model artifacts.
Each: owner, effective date, review cycle, traceable to a driver.
```

Common pitfalls: a charter with no **authority** clause; and a catalog with no **owner** or
**classification** per dataset.

## Security and Best Practices

Classify every catalog entry (public / internal / restricted / PII) and bind access and
retention to the classification. Keep policies **versioned** and **published**. Treat the
public open-data inventory as a governed deliverable, not an afterthought.

## Hands-On Lab

Deliverable walkthroughs. **Shared prerequisites for Labs 3.1–3.5** — a shell with `python3`;
Lab 3.4 also uses `sqlite3`. Each lab produces an artifact. **Cost:** none.

### Lab 3.1 — Author a governance charter

**Objective:** Draft the founding charter skeleton.

```python
python3 - <<'PY'
charter={
 "name":"Agency Data Governance Charter v1.0",
 "purpose":"Govern agency data to serve mission, transparency, and compliance",
 "authority":"Chartered by the Agency Data Governance Council",
 "scope":"All agency datasets and systems of record",
 "drivers":["Service delivery","Open data","Transparency","Risk & compliance"],
 "bodies":["Data Governance Council","Data Stewards"],
 "review":"Annual",
}
for k,v in charter.items(): print(f"{k:10}: {v}")
PY
```

**Expected result:** a charter stating **purpose, authority, scope, drivers, bodies, review**
— the program's mandate.

**Negative test:** publish a charter with no **authority** line; without stated authority the
program cannot enforce policy — add the chartering body.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 3.2 — Write a data policy

**Objective:** Author an enforceable classification policy.

```python
python3 - <<'PY'
policy={
 "id":"POL-CLASS-01","title":"Data Classification Policy","owner":"Chief Data Officer",
 "effective":"2026-07-28","review_cycle_months":12,
 "rules":["Classify every dataset as Public/Internal/Restricted/PII",
          "Bind access and retention to classification",
          "Review classification on data change"],
}
print(policy["id"],policy["title"],"owner:",policy["owner"])
for r in policy["rules"]: print(" -",r)
PY
```

**Expected result:** a policy with **id, owner, effective date, review cycle, rules** — an
enforceable standard.

**Negative test:** issue a policy with no owner or review date; unowned policies rot — assign
both.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 3.3 — Catalog a dataset with metadata

**Objective:** Create an authoritative catalog entry.

```python
python3 - <<'PY'
import json
entry={
 "dataset":"benefits_enrollment","owner":"Benefits Division",
 "steward":"J. Rivera","classification":"PII",
 "system_of_record":"BENSYS","update_frequency":"daily",
 "open_data":False,"retention":"7 years then archive (NARA schedule)",
 "lineage":["intake_form","eligibility_engine","benefits_enrollment"],
}
print(json.dumps(entry,indent=2))
PY
```

**Expected result:** a metadata-rich catalog entry (**owner, steward, classification, SoR,
retention, lineage**) — a governed inventory record.

**Negative test:** catalog a dataset with only a name; without **owner and classification**
it cannot be governed — populate the metadata.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 3.4 — Data-quality scorecard

**Objective:** Measure quality dimensions with a query.

```bash
sqlite3 :memory: <<'SQL'
CREATE TABLE benefits(id INTEGER, ssn TEXT, dob TEXT, county TEXT);
INSERT INTO benefits VALUES (1,'xxx','1980-01-01','Adams'),(2,NULL,'1975-05-05','Adams'),
                            (3,'yyy',NULL,'Zzz'),(4,'zzz','1990-09-09','Adams');
SELECT 'completeness_ssn %' AS metric, ROUND(100.0*COUNT(ssn)/COUNT(*),1) AS value FROM benefits
UNION ALL
SELECT 'completeness_dob %', ROUND(100.0*COUNT(dob)/COUNT(*),1) FROM benefits;
SQL
```

**Expected result:** completeness percentages per column (SSN 75.0, DOB 75.0) — a measurable
**data-quality scorecard**.

**Negative test:** assert "the data is good" with no metric; quality must be **measured**
against dimensions and thresholds — compute the scorecard.

**Rollback:** none (in-memory database).

### Lab 3.5 — Deliverables register

**Objective:** Track the deliverables and their review cycles.

```python
python3 - <<'PY'
register=[
 ("Charter","CDO","Annual"),("Classification Policy","CDO","Annual"),
 ("Data Catalog","Stewards","Continuous"),("DQ Scorecard","Stewards","Monthly"),
 ("Stewardship RACI","Council","Annual"),
]
for name,owner,cycle in register: print(f"{name:22} owner={owner:9} review={cycle}")
PY
```

**Expected result:** a register of the five deliverables with **owners and review cycles** —
proof the program is operating.

**Negative test:** keep deliverables in scattered documents with no register; a **central
register** is what auditors and the exam expect.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The core deliverables — charter, policies and standards, catalog/metadata, a data-quality
framework and scorecard, and stewardship operating-model artifacts — turn drivers into
operations. Each must be owned, dated, reviewed, and traceable to a driver, and prefer
machine-readable forms that can be audited and automated.

- [ ] I can author a governance charter with an authority clause.
- [ ] I can write an owned, dated, reviewable policy.
- [ ] I can catalog a dataset with governing metadata.
- [ ] I can compute a data-quality scorecard.
- [ ] I completed Labs 3.1–3.5 including each negative test.
