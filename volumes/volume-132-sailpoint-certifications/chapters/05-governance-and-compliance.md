# Chapter 05: Governance and Compliance — Certifications, Policies, and Audit

## Learning Objectives

- Run access certification campaigns and interpret their outcomes.
- Write and evaluate separation-of-duties (SoD) policies.
- Produce audit evidence that answers "who had access to what, and who approved it?"
- Recognize rubber-stamping and design campaigns that resist it.

## Governance is the point of IGA

**Supporting Governance** is a named domain on every SailPoint certification. Provisioning gets access to people; governance proves that the access is *appropriate* — and proving it is what auditors, SOX, HIPAA, PCI DSS, and GDPR actually require.

Three mechanisms carry the weight:

| Mechanism | Question it answers |
|:---|:---|
| **Access certification (review) campaign** | Is this access still appropriate? Who said so, and when? |
| **Policy (SoD and more)** | Is this combination of access forbidden? |
| **Audit trail** | Who had what, when, granted by whom, approved by whom? |

## Certification campaigns

A **campaign** asks a reviewer — usually the manager, sometimes the access owner or application owner — to **certify** (approve) or **revoke** each access item, within a deadline. Common campaign types:

| Campaign type | Scope |
|:---|:---|
| **Manager** | Everything each manager's reports hold |
| **Source/application owner** | All access on one application |
| **Role membership** | Everyone who holds a given role |
| **Event-based** | Triggered by a mover event — review what should have been revoked |

The chronic failure is **rubber-stamping**: reviewers approve everything to clear the queue. The countermeasures are design choices — scope campaigns small, present business-meaningful names (Chapter 03's access model), highlight anomalies and privileged access, require a justification to *keep* unusual access, and measure the approve-all rate per reviewer.

## Separation of duties

An **SoD policy** forbids a *combination* of access, because holding both sides of a transaction enables fraud: create a vendor and approve payments to it; raise a purchase order and approve it; write code and deploy it to production unreviewed.

Policies need a **violation workflow**: detect, notify, remediate (revoke one side), or record an approved, time-bound **mitigating control** with compensating oversight. A policy without a remediation path is a report nobody actions.

## Hands-On Lab

Python models the governance controls. **Cost:** none.

### Lab 5.1 — Run an access certification campaign

**Objective:** Execute a manager campaign and read its results.

```bash
python3 - <<'EOF'
campaign = [
  {"identity":"Jane Doe","access":"General Ledger - RW","last_used_days":3,   "privileged":False},
  {"identity":"Jane Doe","access":"Treasury Ops",       "last_used_days":400, "privileged":True},
  {"identity":"Sam Lee", "access":"Salesforce - Read",  "last_used_days":10,  "privileged":False},
  {"identity":"Sam Lee", "access":"Domain Admins",      "last_used_days":365, "privileged":True},
]
def recommend(item):
    if item["privileged"] and item["last_used_days"] > 90:
        return "REVOKE (privileged + unused >90d)"
    if item["last_used_days"] > 180:
        return "REVOKE (unused >180d)"
    return "certify (in active use)"

print("=== MANAGER CERTIFICATION CAMPAIGN ===")
revokes = 0
for item in campaign:
    rec = recommend(item)
    revokes += rec.startswith("REVOKE")
    flag = " <-- FLAG" if rec.startswith("REVOKE") else ""
    print(f"{item['identity']:10} {item['access']:22} last used {item['last_used_days']:>4}d -> {rec}{flag}")
print(f"\n{revokes} of {len(campaign)} items recommended for revocation.")
print("Decisions are recorded with reviewer + timestamp = the audit evidence.")
EOF
```

**Expected result:** Two items are flagged — Jane's year-unused Treasury Ops and Sam's `Domain Admins` — both privileged and stale. The platform's job is not to decide but to **put the right evidence in front of the reviewer** (last-used, privileged flag) so certify-or-revoke is an informed judgment. The recorded decision, with reviewer and timestamp, is the artifact the auditor wants.

**Negative test:** A campaign listing only entitlement names with no usage or risk context — the reviewer has no basis to revoke anything, so they certify everything, and the control produces evidence of a process rather than evidence of appropriate access.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 5.2 — Evaluate separation-of-duties policies

**Objective:** Detect toxic access combinations.

```bash
python3 - <<'EOF'
sod_policies = [
  {"name":"Vendor fraud",   "left":"Vendor Master - Maintain", "right":"Payments - Approve",
   "risk":"Create a fake vendor and pay it"},
  {"name":"PO self-approve","left":"Purchase Order - Create",  "right":"Purchase Order - Approve",
   "risk":"Raise and approve your own spend"},
  {"name":"Unreviewed deploy","left":"Code - Commit",          "right":"Production - Deploy",
   "risk":"Ship code to production with no review"},
]
identities = {
  "Jane Doe": {"General Ledger - RW","Vendor Master - Maintain","Payments - Approve"},
  "Sam Lee":  {"Purchase Order - Create","Salesforce - Read"},
  "Raj Patel":{"Code - Commit","Production - Deploy"},
}
for person, access in identities.items():
    violations = [p for p in sod_policies if p["left"] in access and p["right"] in access]
    if violations:
        for v in violations:
            print(f"VIOLATION  {person}: '{v['name']}' — holds both '{v['left']}' and '{v['right']}'")
            print(f"           risk: {v['risk']}")
            print(f"           remediate: revoke one side, or record a time-bound mitigating control")
    else:
        print(f"clean      {person}")
EOF
```

**Expected result:** Jane violates the vendor-fraud policy and Raj the unreviewed-deploy policy; Sam is clean because he holds only one side. Each finding carries its **business risk** and a **remediation path** — that pairing is what turns a policy from a report into a control. Note that neither violation requires anyone to have done anything wrong: SoD governs *capability*, not behavior.

**Negative test:** Defining SoD policies but never wiring a remediation workflow — violations accumulate in a dashboard, and at audit you must explain why you detected fraud-enabling access and left it in place, which is worse than not having looked.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 5.3 — Produce audit evidence

**Objective:** Answer the auditor's question with a defensible trail.

```bash
python3 - <<'EOF'
audit_log = [
  {"ts":"2026-01-15","identity":"Jane Doe","access":"General Ledger - RW","action":"GRANTED",
   "requested_by":"Jane Doe","approved_by":"R. Patel (manager)","reason":"Role: Financial Analyst"},
  {"ts":"2026-04-02","identity":"Jane Doe","access":"Treasury Ops","action":"GRANTED",
   "requested_by":"Jane Doe","approved_by":"T. Owner (access owner)","reason":"Project: year-end"},
  {"ts":"2026-08-01","identity":"Jane Doe","access":"Treasury Ops","action":"REVOKED",
   "requested_by":"campaign-2026-Q3","approved_by":"R. Patel (manager)","reason":"Unused 400 days"},
]
print("=== ACCESS HISTORY: Jane Doe ===")
for e in audit_log:
    print(f"{e['ts']}  {e['action']:8} {e['access']:22} approved_by={e['approved_by']:28} ({e['reason']})")

held_now = {e["access"] for e in audit_log if e["action"]=="GRANTED"} - \
           {e["access"] for e in audit_log if e["action"]=="REVOKED"}
print(f"\nCurrently holds: {sorted(held_now)}")
print("Auditor's questions answered: what, when, who requested, who approved, why, and when removed.")
EOF
```

**Expected result:** A complete chronology — granted, approved by a named person with a reason, later revoked by a named campaign. Reconstructing current access from the event history (rather than trusting a snapshot) is what makes the evidence defensible: the state and the trail agree by construction. This is the "who had access to what" answer that governance exists to produce.

**Negative test:** Keeping only current-state data with no history — you can say what Jane has today but not who approved it or when, and an auditor cannot verify that any control ever operated.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] Certification campaigns run, with usage and risk context that resists rubber-stamping.
- [ ] SoD policies evaluated, with business risk and a remediation path.
- [ ] Audit evidence produced: what, when, requested by, approved by, why, revoked when.
- [ ] Campaign types matched to their governance purpose.
