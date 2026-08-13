# Chapter 02: The Identity Data Model and Sources

## Learning Objectives

- Explain the identity data model: identities, accounts, entitlements, and attributes.
- Describe sources, aggregation, correlation, and the authoritative source.
- Recognize and resolve orphan and uncorrelated accounts.
- Model aggregation and correlation in free Python.

## Sources — where identity data comes from

The **Sources** domain appears on every SailPoint certification, because nothing else in IGA works until the data is right. A **source** (called an *application* in IdentityIQ) is any connected system that holds accounts: Active Directory, Entra ID, Workday, a database, a SaaS app, a mainframe.

Two source roles matter:

| Source role | Purpose |
|:---|:---|
| **Authoritative source** | The system of record for *who exists* — usually HR (Workday, SuccessFactors). It creates and terminates identities. |
| **Non-authoritative (target) source** | Systems where people hold *accounts and access* — AD, Salesforce, a database. These contribute accounts and entitlements, not existence. |

Getting this wrong is the classic deployment error: if AD is treated as authoritative, a contractor deleted in HR keeps their identity because their AD account still exists — and the leaver process never fires.

## The identity data model

SailPoint's model has four layers, and the vocabulary is exam-relevant:

| Object | What it is |
|:---|:---|
| **Identity** | A person (or non-human actor). In IdentityIQ this is the *Identity Cube*. Holds identity attributes (department, manager, location, lifecycle state). |
| **Account** | A login on one source, belonging to an identity (`jdoe` in AD, `j.doe@corp` in Salesforce). |
| **Entitlement** | A unit of access held by an account — a group membership, a role in an app, a permission. |
| **Attribute** | A field on an identity or account, often *mapped* from a source attribute and used to drive logic. |

The core value is **correlation**: one person's many accounts, collapsed into a single identity, so a question like "what does Jane have?" has one answer.

## Aggregation and correlation

**Aggregation** reads accounts and entitlements from a source. **Correlation** attaches each aggregated account to the right identity, using a correlation rule (match `employeeId`, or `sAMAccountName` to a mapped attribute).

Two failure modes have specific names and matter to auditors:

- **Uncorrelated account** — an account that aggregated but matched no identity. Usually a data-quality problem (missing `employeeId`).
- **Orphan account** — an account with no valid owner at all: the classic ex-employee's account that still works. Orphans are an audit finding *and* a real attack path.

## Hands-On Lab

Python models the identity data model. **Cost:** none.

### Lab 2.1 — Aggregate and correlate accounts into identities

**Objective:** Build the correlation step every SailPoint deployment depends on.

```bash
python3 - <<'EOF'
# Authoritative source (HR) defines WHO EXISTS
hr = [
  {"employeeId":"E100","name":"Jane Doe","dept":"Finance","manager":"E200","status":"Active"},
  {"employeeId":"E200","name":"Raj Patel","dept":"Finance","manager":None,"status":"Active"},
  {"employeeId":"E300","name":"Sam Lee","dept":"Sales","manager":"E200","status":"Terminated"},
]
# Target sources contribute ACCOUNTS + ENTITLEMENTS
accounts = [
  {"source":"AD","account":"jdoe","employeeId":"E100","entitlements":["Domain Users","Finance-RW"]},
  {"source":"Salesforce","account":"j.doe","employeeId":"E100","entitlements":["Sales-Read"]},
  {"source":"AD","account":"rpatel","employeeId":"E200","entitlements":["Domain Users","Finance-Admin"]},
  {"source":"AD","account":"slee","employeeId":"E300","entitlements":["Domain Users","Sales-RW"]},
  {"source":"AD","account":"svc_backup","employeeId":None,"entitlements":["Domain Admins"]},
]
identities = {h["employeeId"]: {**h, "accounts": []} for h in hr}
uncorrelated = []
for acct in accounts:
    ident = identities.get(acct["employeeId"])
    (ident["accounts"].append(acct) if ident else uncorrelated.append(acct))

for eid, i in identities.items():
    held = sorted({e for a in i["accounts"] for e in a["entitlements"]})
    print(f"{eid} {i['name']:10} [{i['status']:10}] accounts={[a['account'] for a in i['accounts']]} entitlements={held}")
print("\nUNCORRELATED (no matching identity):", [a["account"] for a in uncorrelated])
print("ORPHAN RISK: 'slee' belongs to a TERMINATED identity but still holds Sales-RW")
EOF
```

**Expected result:** Jane Doe's AD and Salesforce accounts collapse into one identity holding three entitlements; `svc_backup` is **uncorrelated** (it has `Domain Admins` and no owner); and `slee` is an **orphan risk** — a terminated identity whose account still carries access. Those last two lines are exactly what an access-review campaign and a leaver process exist to catch. Correlation is what turns scattered account data into a governable identity.

**Negative test:** Aggregating without a correlation rule — every account becomes uncorrelated, and the identity warehouse is useless: you cannot answer "what does Jane have?" because nothing is joined to Jane.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 2.2 — Identity attributes and the authoritative source

**Objective:** Show why the authoritative source must define existence.

```bash
python3 - <<'EOF'
def lifecycle_from_hr(hr_status):
    return {"Active":"active", "Leave":"inactive", "Terminated":"terminated"}.get(hr_status, "unknown")

records = [("E100","Active"), ("E300","Terminated"), ("E400","Leave")]
for eid, status in records:
    print(f"{eid}: HR status {status:10} -> identity lifecycle state '{lifecycle_from_hr(status)}'")

print("\nIf AD (not HR) were authoritative, E300 would still 'exist' because its AD account exists,")
print("the leaver process would never fire, and the orphan account would persist indefinitely.")
EOF
```

**Expected result:** HR status maps cleanly to a lifecycle state, which is what drives joiner-mover-leaver automation in Chapter 04. The closing lines state the design rule: **existence flows from the authoritative source**, never from a target system. This mapping — source attribute to identity attribute — is the "identity data management" material the Identity Security Professional credential tests.

**Negative test:** Two competing authoritative sources (HR *and* a contractor database) with no precedence rule — identities duplicate, and the same human appears twice with different access.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 2.3 — Find orphan and uncorrelated accounts

**Objective:** Produce the data-quality report every deployment runs continuously.

```bash
python3 - <<'EOF'
accounts = [
  {"account":"jdoe","owner":"E100","owner_status":"Active","privileged":False},
  {"account":"slee","owner":"E300","owner_status":"Terminated","privileged":False},
  {"account":"svc_backup","owner":None,"owner_status":None,"privileged":True},
  {"account":"admin_old","owner":None,"owner_status":None,"privileged":True},
]
for a in accounts:
    if a["owner"] is None:
        sev = "CRITICAL" if a["privileged"] else "HIGH"
        print(f"{sev:8} UNCORRELATED: {a['account']} — no identity owner{' (PRIVILEGED)' if a['privileged'] else ''}")
    elif a["owner_status"] == "Terminated":
        print(f"CRITICAL ORPHAN:  {a['account']} — owner {a['owner']} is Terminated but access remains")
    else:
        print(f"OK               {a['account']} — owned by {a['owner']}")
print("\nRemediation: assign an owner (service accounts need a human owner) or deprovision.")
EOF
```

**Expected result:** Two uncorrelated accounts flagged (both privileged, hence CRITICAL) and one orphan whose terminated owner still has live access. This report is the first thing an IGA program produces and the first thing an auditor asks for. Service accounts are the perennial offender: they legitimately have no human *user*, so they must be assigned a human **owner** to be governable.

**Negative test:** Treating every uncorrelated account as noise and suppressing the report — `svc_backup` holds `Domain Admins` with no accountable owner, which is precisely the account an attacker wants.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] Identity, account, entitlement, and attribute defined and distinguished.
- [ ] Authoritative vs target sources understood, and why HR defines existence.
- [ ] Aggregation and correlation modeled end to end.
- [ ] Orphan and uncorrelated accounts detected and remediated.
