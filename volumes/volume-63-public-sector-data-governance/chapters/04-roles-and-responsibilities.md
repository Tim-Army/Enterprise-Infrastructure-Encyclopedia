# Chapter 04: Data Governance Roles and Responsibilities

## Learning Objectives

- Describe the governance bodies of a public-sector program.
- Define the core roles (CDO, data owner, steward, custodian) and their duties.
- Build a RACI matrix for governance decisions and deliverables.
- Plan stakeholder engagement and change management.
- Complete a walkthrough for each Roles and Responsibilities sub-topic.

## Theory and Architecture

Governance runs on **people and decision rights**, not documents alone. A public-sector
program defines: **governing bodies** — a **Data Governance Council/Board** (executive
sponsors and division leaders who set policy and arbitrate) and often working groups; and
**roles** — the **Chief Data Officer (CDO)** (accountable executive, often legally mandated in
government), **data owners** (accountable for a data domain), **data stewards** (day-to-day
quality and metadata), and **data custodians** (IT operators of the systems). The tool for
making this unambiguous is a **RACI** matrix — for each decision or deliverable, exactly one
**Accountable** party, the **Responsible** doers, those **Consulted**, and those **Informed**.
Because government programs cross agencies and involve the public, **stakeholder engagement
and change management** are first-class responsibilities, not optional.

## Design Considerations

Assign **one Accountable** per decision — split accountability stalls governance. Separate
**owner** (accountable for the data) from **custodian** (runs the system) so business and IT
duties are clear. Size the Council to decide, not to admire problems. Plan engagement for
both internal staff and, where open data is involved, the public.

## Implementation and Automation

The labs define the bodies, a role catalog, a RACI matrix, and an engagement plan.

## Validation and Troubleshooting

Confirm the role model:

```text
Bodies: Data Governance Council/Board (+ working groups).
Roles : CDO (accountable exec) > Data Owner (domain) > Steward (quality/metadata) > Custodian (IT).
Tool  : RACI — exactly ONE Accountable per decision/deliverable.
```

Common pitfalls: **two Accountable** parties (nobody decides); and conflating **owner** and
**custodian** so quality issues bounce between business and IT.

## Security and Best Practices

Bind **access approval** to the data **owner** and **operation** to the **custodian** —
separation of duties. Document roles in the charter and review as the org changes. Engage
stakeholders early; governance imposed without buy-in fails.

## Hands-On Lab

Roles walkthroughs. **Shared prerequisites for Labs 4.1–4.4** — a shell with `python3`. Each
lab produces a governance artifact. **Cost:** none.

### Lab 4.1 — Define the governing bodies

**Objective:** Charter the council and working groups.

```python
python3 - <<'PY'
bodies={
 "Data Governance Council":{"members":["CDO(chair)","Division leaders","CISO","Privacy Officer"],
   "decides":["Policy approval","Priorities","Escalations"]},
 "Data Quality Working Group":{"members":["Stewards","Analysts"],
   "decides":["DQ rules","Thresholds"]},
}
for b,info in bodies.items():
    print(b); print("  members:",", ".join(info["members"])); print("  decides:",", ".join(info["decides"]))
PY
```

**Expected result:** a **council** (policy/escalation) and a **working group** (execution) —
the decision structure.

**Negative test:** run governance with no standing body; ad-hoc decisions have no authority —
charter a council.

**Cleanup:** none.

### Lab 4.2 — Role catalog

**Objective:** Distinguish owner, steward, and custodian.

```python
python3 - <<'PY'
roles={
 "CDO":"Accountable executive for data as an asset; often legally mandated",
 "Data Owner":"Accountable for a data domain; approves access and classification",
 "Data Steward":"Day-to-day data quality, metadata, and issue resolution",
 "Data Custodian":"IT operation of the systems that store/process the data",
}
for r,d in roles.items(): print(f"{r:14}: {d}")
PY
```

**Expected result:** four distinct roles with clear duties — **owner ≠ custodian**.

**Negative test:** make IT the "owner" of business data; **owners are accountable business
leaders**, custodians run the systems — separate them.

**Cleanup:** none.

### Lab 4.3 — Build a RACI matrix

**Objective:** Assign decision rights with one Accountable each.

```python
python3 - <<'PY'
raci={
 "Approve classification policy":{"A":"CDO","R":["Stewards"],"C":["Privacy Officer"],"I":["Council"]},
 "Fix a data-quality defect":{"A":"Data Owner","R":["Steward","Custodian"],"C":["Analyst"],"I":["CDO"]},
}
for decision,m in raci.items():
    assert isinstance(m["A"],str), "exactly one Accountable"
    print(f"{decision}: A={m['A']} R={m['R']} C={m['C']} I={m['I']}")
print("check: one Accountable per row -> OK")
PY
```

**Expected result:** a RACI with **exactly one Accountable** per decision — unambiguous
decision rights.

**Negative test:** list two Accountable parties for a decision; governance stalls — enforce
one A per row.

**Cleanup:** none.

### Lab 4.4 — Stakeholder engagement plan

**Objective:** Plan change management for a new policy.

```python
python3 - <<'PY'
plan=[
 ("Executives","Brief + endorse","Before rollout"),
 ("Division staff","Training + FAQ","At rollout"),
 ("IT custodians","Runbook changes","At rollout"),
 ("Public (open data)","Portal notice","On publish"),
]
for who,how,when in plan: print(f"{who:22} {how:22} {when}")
PY
```

**Expected result:** an engagement plan covering internal and (for open data) public
stakeholders — adoption, not just issuance.

**Negative test:** publish a policy with no engagement; governance imposed without buy-in is
ignored — plan the rollout.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Governance is decision rights made explicit: a council and working groups; distinct CDO,
owner, steward, and custodian roles; a RACI with exactly one Accountable per decision; and a
stakeholder-engagement plan that drives adoption. Separate owner from custodian and never
split accountability.

- [ ] I can charter the governing bodies.
- [ ] I can distinguish owner, steward, and custodian.
- [ ] I can build a single-Accountable RACI matrix.
- [ ] I can plan stakeholder engagement and change.
- [ ] I completed Labs 4.1–4.4 including each negative test.
