# Chapter 06: The DGSP Core Body of Knowledge

## Learning Objectives

- Explain how the Data Governance and Stewardship Professional (DGSP) core underpins PSDGP.
- Apply the core data-management concepts: quality, metadata, master data, lifecycle, security.
- Relate each concept to a public-sector governance obligation.
- Complete a walkthrough for each core-concept sub-topic.
- Use the core body of knowledge to satisfy the PSDGP prerequisite path.

## Theory and Architecture

PSDGP's alternate prerequisite is a **'core'-level ICCP certification** — chiefly the **Data
Governance and Stewardship Professional (DGSP)**. Whether you take DGSP or the degree-plus-
experience path, the exam assumes fluency in the **general data-management body of knowledge**
that public-sector governance specializes: (1) **data quality** — the dimensions
(completeness, accuracy, timeliness, consistency, validity, uniqueness) and how they are
measured; (2) **metadata** — business, technical, and operational metadata, and lineage; (3)
**master and reference data (MDM)** — a single authoritative version of core entities (person,
place, organization); (4) the **data lifecycle** — create, store, use, share, archive, dispose;
and (5) **data security and privacy** — classification, access control, and protection. In
government these map directly to obligations: quality → service delivery; metadata → FOIA
findability; MDM → cross-agency consistency; lifecycle → records retention; security →
FISMA/privacy.

## Design Considerations

Do not treat the core as separate from the public-sector layer — **each core concept exists to
satisfy a driver and a law**. Measure quality against thresholds, keep metadata authoritative,
master the entities that cross programs, and make lifecycle disposition follow the retention
schedule.

## Implementation and Automation

The labs exercise the six quality dimensions, metadata/lineage, an MDM golden-record match, a
lifecycle stage machine, and a classification-to-control binding.

## Validation and Troubleshooting

Confirm the core map:

```text
Quality  -> 6 dimensions, measured vs thresholds  (driver: service delivery)
Metadata -> business/technical/operational + lineage  (driver: FOIA findability)
MDM      -> golden record for person/place/org  (driver: cross-agency consistency)
Lifecycle-> create->store->use->share->archive->dispose  (driver: retention)
Security -> classify -> access control -> protect  (driver: FISMA/privacy)
```

Common pitfalls: measuring only **completeness** and calling it quality; and an MDM with
**no survivorship rule** for conflicting records.

## Security and Best Practices

Bind **classification** (from the core) to **access and retention** (from the legal layer) so
one metadata attribute drives protection and disposition. Keep master data authoritative to
avoid conflicting citizen records across programs.

## Hands-On Lab

Core-concept walkthroughs. **Shared prerequisites for Labs 6.1–6.5** — a shell with `python3`.
**Cost:** none.

### Lab 6.1 — Measure the six quality dimensions

**Objective:** Score a dataset beyond completeness.

```python
python3 - <<'PY'
rows=[{"id":1,"ssn":"111","dob":"1980-01-01"},{"id":2,"ssn":None,"dob":"1980-01-01"},
      {"id":3,"ssn":"111","dob":"bad-date"}]
n=len(rows)
completeness=100*sum(1 for r in rows if r["ssn"])/n
uniqueness=100*len({r["ssn"] for r in rows if r["ssn"]})/max(1,sum(1 for r in rows if r["ssn"]))
validity=100*sum(1 for r in rows if len(str(r["dob"]))==10 and str(r["dob"])[4]=="-")/n
print(f"completeness={completeness:.0f}%  uniqueness={uniqueness:.0f}%  validity={validity:.0f}%")
PY
```

**Expected result:** distinct scores per dimension (completeness 67%, uniqueness 50%, validity
67%) — quality is **multi-dimensional**.

**Negative test:** report only completeness; duplicates and invalid dates hide — measure
**several dimensions**.

**Cleanup:** none.

### Lab 6.2 — Classify metadata and lineage

**Objective:** Separate metadata types and record lineage.

```python
python3 - <<'PY'
meta={"business":{"definition":"Enrolled beneficiary"},
      "technical":{"type":"table","pk":"id"},
      "operational":{"last_load":"2026-07-28","rows":10432}}
lineage=["intake_form","eligibility_engine","benefits_enrollment"]
for k,v in meta.items(): print(f"{k:11}: {v}")
print("lineage:"," -> ".join(lineage))
PY
```

**Expected result:** **business/technical/operational** metadata plus a lineage chain — the
findability layer FOIA depends on.

**Negative test:** keep only technical metadata; without **business** definitions the public
and FOIA officers cannot understand the data — capture all three.

**Cleanup:** none.

### Lab 6.3 — MDM golden record

**Objective:** Resolve conflicting records with a survivorship rule.

```python
python3 - <<'PY'
records=[{"src":"DMV","name":"J RIVERA","updated":"2025-01-01"},
         {"src":"BENSYS","name":"Jose Rivera","updated":"2026-06-01"}]
golden=max(records,key=lambda r:r["updated"])  # survivorship: most recent wins
print("golden record:",golden["name"],"(from",golden["src"]+")")
PY
```

**Expected result:** one **golden record** chosen by a survivorship rule — a single
authoritative citizen identity across programs.

**Negative test:** keep both records as equally true; conflicting identities break service and
reporting — apply an MDM **survivorship** rule.

**Cleanup:** none.

### Lab 6.4 — Data lifecycle state machine

**Objective:** Model lifecycle stages ending in disposition.

```python
python3 - <<'PY'
stages=["create","store","use","share","archive","dispose"]
nxt={a:b for a,b in zip(stages,stages[1:])}
s="use"
while s in nxt: print(s,"->",nxt[s]); s=nxt[s]
print("terminal:",s)
PY
```

**Expected result:** a lifecycle advancing **use → share → archive → dispose** — disposition
that honors the retention schedule.

**Negative test:** keep data forever "just in case"; retention law requires **disposition** —
model the terminal stage.

**Cleanup:** none.

### Lab 6.5 — Bind classification to controls

**Objective:** Drive protection from one metadata attribute.

```python
python3 - <<'PY'
CONTROLS={"Public":{"access":"anyone","retention":"per schedule"},
          "PII":{"access":"need-to-know + audit","retention":"per schedule + secure destroy"}}
for cls in ["Public","PII"]:
    print(cls,"->",CONTROLS[cls])
PY
```

**Expected result:** classification drives **access and retention** automatically — core
metadata enforcing the legal layer.

**Negative test:** set access per dataset by hand; **classification-driven** control is
consistent and auditable — bind it.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The DGSP core — data quality, metadata, master data, lifecycle, and security — is the general
body of knowledge PSDGP specializes for government. Each concept satisfies a public-sector
driver and law: quality serves delivery, metadata enables FOIA, MDM gives cross-agency
consistency, lifecycle honors retention, and classification drives security and privacy.

- [ ] I can measure several data-quality dimensions.
- [ ] I can classify metadata types and record lineage.
- [ ] I can produce an MDM golden record.
- [ ] I can model the lifecycle and bind classification to controls.
- [ ] I completed Labs 6.1–6.5 including each negative test.
