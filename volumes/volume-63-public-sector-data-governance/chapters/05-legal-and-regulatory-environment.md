# Chapter 05: The Legal and Regulatory Environment

## Learning Objectives

- Map the major U.S. public-sector data laws to governance obligations.
- Handle FOIA/open-records and privacy (Privacy Act/PII) duties.
- Apply records management and retention (Federal Records Act / NARA).
- Relate security and compliance frameworks (FISMA / NIST 800-53 / FedRAMP) to governance.
- Complete a walkthrough for each Legal and Regulatory sub-topic.

## Theory and Architecture

The legal environment is what most distinguishes public-sector governance. Five bodies of law
and policy recur: (1) **transparency / open records** — the **Freedom of Information Act
(FOIA)** and state equivalents require agencies to disclose records on request within
deadlines; (2) **privacy** — the **Privacy Act of 1974**, plus PII-protection rules and (for
specific data) HIPAA/FERPA, govern collection, use, and disclosure of personal data; (3)
**records management** — the **Federal Records Act** and **NARA** schedules dictate what is a
record, how long it is kept, and when it is destroyed or archived; (4) **security and
compliance** — **FISMA**, **NIST SP 800-53** controls, and **FedRAMP** for cloud set the
security baseline; and (5) **data sharing and openness** — the **Foundations for
Evidence-Based Policymaking Act (Evidence Act)** and the **OPEN Government Data Act** require
open, machine-readable data and data inventories, balanced against the above. Governance
exists to make these obligations **operational and auditable**.

## Design Considerations

Bind each obligation to a **deliverable and a role**: FOIA → a findable catalog + a records
officer; privacy → classification + the Privacy Officer; retention → NARA schedules + stewards.
Where laws tension (open data vs privacy), **privacy and security constrain openness** — publish
aggregated or redacted data. Track legal changes; statute drives scope.

## Implementation and Automation

The labs implement a FOIA-readiness check, a PII classifier, a retention schedule, a
security-control mapping, and an open-data compliance check.

## Validation and Troubleshooting

Confirm the legal map:

```text
FOIA/open records -> disclose on request (deadlines); findable catalog.
Privacy Act / PII -> lawful collection/use/disclosure; classify & protect.
Federal Records Act / NARA -> record definition, retention schedule, disposition.
FISMA / NIST 800-53 / FedRAMP -> security baseline (incl. cloud).
Evidence Act / OPEN Gov Data Act -> open, machine-readable data + inventory.
```

Common pitfalls: destroying records **before** their NARA schedule (a Federal Records Act
violation); and publishing open data **without** a privacy review.

## Security and Best Practices

Make **retention** and **privacy** authoritative in the catalog so disposition and disclosure
are automatic, not manual judgment calls. Keep a defensible **audit trail** for FOIA and
records disposition. Treat security compliance (FISMA/NIST/FedRAMP) as a governance input, not
a separate silo.

## Hands-On Lab

Legal/regulatory walkthroughs. **Shared prerequisites for Labs 5.1–5.5** — a shell with
`python3`. Each lab produces a compliance artifact. **Cost:** none.

### Lab 5.1 — FOIA-readiness check

**Objective:** Test whether a dataset can answer a FOIA request quickly.

```python
python3 - <<'PY'
def foia_ready(has_catalog_entry, has_owner, is_findable, exempt):
    if exempt: return "withhold/redact per exemption"
    return "ready to disclose" if (has_catalog_entry and has_owner and is_findable) else "NOT ready (fix catalog/owner/findability)"
print("Budget data:", foia_ready(True,True,True,False))
print("Investigation file:", foia_ready(True,True,True,True))
PY
```

**Expected result:** disclosable data is **ready** when cataloged/owned/findable; exempt data
is **withheld/redacted** — FOIA operationalized.

**Negative test:** claim FOIA-ready with no catalog entry; if records cannot be **found** the
deadline is missed — catalog first.

**Cleanup:** none.

### Lab 5.2 — Classify PII under the Privacy Act

**Objective:** Flag personal data for protection.

```python
python3 - <<'PY'
PII_FIELDS={"ssn","dob","address","email","phone","medical","biometric"}
def classify(fields):
    hit=PII_FIELDS & set(fields)
    return ("PII" if hit else "Non-PII"), sorted(hit)
for cols in [["id","ssn","county"],["id","county","total"]]:
    label,hit=classify(cols); print(cols,"->",label,hit)
PY
```

**Expected result:** datasets containing SSN/DOB/etc. are labeled **PII**; others **Non-PII** —
driving access and disclosure rules.

**Negative test:** treat SSN as ordinary data; the **Privacy Act** requires protection —
classify and restrict PII.

**Cleanup:** none.

### Lab 5.3 — Records-retention schedule

**Objective:** Encode a NARA-style disposition.

```python
python3 - <<'PY'
schedule=[
 {"series":"Benefits case files","retain_years":7,"disposition":"Archive to NARA"},
 {"series":"Routine email","retain_years":3,"disposition":"Destroy"},
 {"series":"Permanent policy records","retain_years":None,"disposition":"Permanent (transfer to NARA)"},
]
for s in schedule:
    r=s["retain_years"]; print(f"{s['series']:26} retain={r if r else 'permanent':>9}  -> {s['disposition']}")
PY
```

**Expected result:** each record series with a **retention period and disposition** — a
defensible schedule.

**Negative test:** delete a case file at year 2; its schedule says **7 years** — early
destruction violates the Federal Records Act.

**Cleanup:** none.

### Lab 5.4 — Map security controls (FISMA/NIST)

**Objective:** Tie governance to the security baseline.

```python
python3 - <<'PY'
mapping={
 "Access to PII datasets":"AC-3 Access Enforcement (NIST 800-53)",
 "Audit of data disclosure":"AU-2 Event Logging",
 "Cloud hosting of agency data":"FedRAMP authorization required",
}
for need,control in mapping.items(): print(f"{need:30} -> {control}")
PY
```

**Expected result:** governance needs mapped to **NIST 800-53 controls / FedRAMP** — security
compliance made explicit.

**Negative test:** host agency data in a non-FedRAMP cloud; federal data requires **FedRAMP
authorization** — verify before onboarding.

**Cleanup:** none.

### Lab 5.5 — Open-data compliance check

**Objective:** Validate a dataset against the OPEN Government Data Act.

```python
python3 - <<'PY'
def open_data_ok(machine_readable, in_inventory, privacy_reviewed, license_open):
    checks={"machine_readable":machine_readable,"in_inventory":in_inventory,
            "privacy_reviewed":privacy_reviewed,"open_license":license_open}
    return all(checks.values()), checks
ok,checks=open_data_ok(True,True,True,True); print("publishable:",ok,checks)
PY
```

**Expected result:** publishable only when **machine-readable, inventoried, privacy-reviewed,
and openly licensed** — the Evidence Act / OPEN Data Act bar.

**Negative test:** publish a PDF that skipped privacy review; open data must be
**machine-readable and privacy-cleared** — fix both before publishing.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The legal environment — FOIA/open records, the Privacy Act/PII, the Federal Records Act/NARA,
FISMA/NIST/FedRAMP, and the Evidence Act/OPEN Government Data Act — is what makes public-sector
governance distinct. Bind each obligation to a deliverable and a role, let privacy and security
constrain openness, and keep disposition and disclosure auditable.

- [ ] I can map the major laws to governance obligations.
- [ ] I can run a FOIA-readiness and PII classification check.
- [ ] I can encode a NARA-style retention schedule.
- [ ] I can map governance to NIST/FedRAMP and check open-data compliance.
- [ ] I completed Labs 5.1–5.5 including each negative test.
