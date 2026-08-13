# Chapter 02: Public Sector Data Governance Mission Drivers

## Learning Objectives

- Explain why a public-sector data governance program exists (its mission drivers).
- Align governance to public value, service delivery, and open-data mandates.
- Connect transparency and accountability drivers to governance scope.
- Trace risk, compliance, and audit drivers into governance priorities.
- Complete a walkthrough for each Mission Drivers sub-topic.

## Theory and Architecture

**Mission drivers** are the reasons a government organization governs its data — the "why"
that every deliverable, role, and policy must trace back to. In the public sector the drivers
differ from commercial ones: agencies exist to deliver **public value and services**, to be
**transparent and accountable** to citizens and oversight bodies, and to comply with
**statute** — not to maximize profit. Four families of drivers recur: (1) **mission/service
delivery** — better data means better programs and outcomes; (2) **data as a strategic asset /
open data** — legal mandates (e.g., the OPEN Government Data Act) require agencies to treat
data as an asset and publish it openly by default; (3) **transparency and accountability** —
FOIA, open records, and audit demand trustworthy, findable data; and (4) **risk, compliance,
and audit** — privacy, security, and records law create obligations whose failure carries
legal and reputational cost. Governance prioritization flows from these drivers.

## Design Considerations

Start a program by **naming the drivers explicitly** and ranking them for the organization.
Every proposed policy, catalog, or role should map to at least one driver; anything that maps
to none is scope creep. Public value and legal compliance usually outrank convenience.

## Implementation and Automation

The labs build a driver inventory, a mission-alignment matrix, an open-data check, and a
risk-driver register — the artifacts that justify the program.

## Validation and Troubleshooting

Confirm the driver model:

```text
Drivers: (1) mission/service delivery; (2) data-as-asset / open data (OPEN Gov Data Act);
(3) transparency & accountability (FOIA/audit); (4) risk, compliance & audit (privacy/security/records).
Rule: every deliverable and role traces to >=1 driver.
```

Common pitfalls: copying a **commercial** driver set (revenue/marketing) into a government
program; and leaving drivers implicit so scope drifts.

## Security and Best Practices

Make **compliance and privacy drivers** first-class, not afterthoughts. Publish the driver
list and the alignment matrix so stakeholders can challenge scope. Revisit drivers when
mandates change (new statute, new administration priorities).

## Hands-On Lab

Mission-driver walkthroughs. **Shared prerequisites for Labs 2.1–2.4** — a shell with
`python3`. Each lab produces a governance artifact. **Cost:** none.

### Lab 2.1 — Build a driver inventory

**Objective:** Enumerate and rank the public-sector drivers.

```python
python3 - <<'PY'
drivers=[
 ("Service delivery","Improve program outcomes with reliable data",5),
 ("Open data / data-as-asset","OPEN Government Data Act: publish open by default",4),
 ("Transparency & accountability","FOIA, open records, oversight, audit",5),
 ("Risk & compliance","Privacy, security, records-retention obligations",5),
]
for name,why,pri in sorted(drivers,key=lambda d:-d[2]):
    print(f"[P{pri}] {name:28} {why}")
PY
```

**Expected result:** a ranked **driver inventory** — the justification baseline for the
program.

**Negative test:** list "increase revenue" as a driver; public agencies govern for **service,
transparency, and compliance** — drop commercial drivers.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 2.2 — Mission-alignment matrix

**Objective:** Map each governance initiative to a driver.

```python
python3 - <<'PY'
initiatives={
 "Data catalog":"Transparency & accountability",
 "Data-quality scorecard":"Service delivery",
 "Open-data portal":"Open data / data-as-asset",
 "Records-retention policy":"Risk & compliance",
}
orphans=[i for i,d in initiatives.items() if not d]
for i,d in initiatives.items(): print(f"{i:26} -> {d}")
print("orphans (no driver):", orphans or "none")
PY
```

**Expected result:** every initiative mapped to a driver with **no orphans** — a defensible
scope.

**Negative test:** add an initiative with no driver; if it maps to nothing it is **scope
creep** — cut it or find its driver.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 2.3 — Open-data "publish by default" check

**Objective:** Classify a dataset for open publication.

```python
python3 - <<'PY'
def openness(dataset, has_pii, is_law_enforcement_sensitive):
    if has_pii or is_law_enforcement_sensitive:
        return "restricted (protect first, publish derived/aggregated)"
    return "open by default (publish)"
for ds,pii,le in [("Budget expenditures",False,False),("Benefits roster",True,False)]:
    print(f"{ds:22}: {openness(ds,pii,le)}")
PY
```

**Expected result:** non-sensitive data **open by default**; PII/sensitive data **restricted**
— the open-data mandate balanced against privacy.

**Negative test:** publish a dataset with PII to satisfy "open by default"; **privacy law
overrides** — aggregate or withhold PII.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 2.4 — Risk-driver register

**Objective:** Record the compliance/audit drivers as risks.

```python
python3 - <<'PY'
risks=[
 {"risk":"FOIA request unmet in time","driver":"Transparency","impact":"legal/reputational"},
 {"risk":"PII breach","driver":"Risk & compliance","impact":"statutory penalty"},
 {"risk":"Records destroyed early","driver":"Risk & compliance","impact":"Federal Records Act violation"},
]
for r in risks: print(f"- {r['risk']:28} [{r['driver']}] -> {r['impact']}")
PY
```

**Expected result:** a **risk register** tied to drivers — feeding governance priorities.

**Negative test:** track risks with no owning driver or law; each public-sector risk should
name the **obligation** it threatens.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Public-sector mission drivers — service delivery, open data, transparency/accountability, and
risk/compliance — are the "why" behind every governance deliverable and role. Name them, rank
them, and map every initiative to at least one; anything unmapped is scope creep.

- [ ] I can explain the four public-sector driver families.
- [ ] I can build a driver inventory and alignment matrix.
- [ ] I can balance open-data mandates against privacy.
- [ ] I can tie compliance risks to drivers.
- [ ] I completed Labs 2.1–2.4 including each negative test.
