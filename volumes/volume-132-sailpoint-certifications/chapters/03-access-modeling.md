# Chapter 03: Access Modeling — Roles, Entitlements, and Access Profiles

## Learning Objectives

- Build an access model: entitlements, access profiles, and roles.
- Compare RBAC and ABAC, and use birthright roles for automatic access.
- Mine roles from existing entitlement data and measure the model's quality.
- Recognize role explosion and the over-entitlement it hides.

## Why model access at all

Raw entitlements are unreadable to the people who must approve them. "Approve `CN=FIN-GL-RW,OU=Groups`?" is a question no manager can answer honestly, so they click approve — the phenomenon that makes access reviews meaningless. The **access model** exists to turn technical entitlements into business-meaningful bundles that a manager *can* judge.

SailPoint's ISC model has three layers:

| Layer | What it is | Example |
|:---|:---|:---|
| **Entitlement** | One unit of access on one source | AD group `FIN-GL-RW` |
| **Access profile** | A bundle of entitlements from **one** source, with a business name | "General Ledger — Read/Write" |
| **Role** | A bundle of **access profiles** (potentially spanning sources), aligned to a job | "Financial Analyst" |

IdentityIQ expresses the same idea with **business roles** (what the job needs) composed of **IT roles** (what the systems grant) — the vocabulary differs, the layering does not.

## RBAC and ABAC

| Model | Access is decided by | Strength | Weakness |
|:---|:---|:---|:---|
| **RBAC** (role-based) | Membership in a role | Reviewable, stable, auditable | Roles multiply as exceptions accumulate |
| **ABAC** (attribute-based) | Attribute rules evaluated at request time (department, location, clearance) | Flexible, fewer objects | Harder to review — the "role" is implicit in a rule |

Real deployments blend them: roles for the reviewable core, attribute-driven **membership criteria** to assign those roles automatically. A **birthright role** is the canonical case — access every member of a population gets automatically (all employees get email and the intranet), assigned by attribute rather than request.

## Role explosion

The failure mode to know by name: every exception becomes a new role until there are more roles than people, and the model stops being reviewable — the exact problem roles were meant to solve. The diagnostic is simple arithmetic (roles per identity, single-member roles), and the fix is to model the common core and handle genuine exceptions as separately-approved, time-bound access rather than new permanent roles.

## Hands-On Lab

Python models the access model. **Cost:** none.

### Lab 3.1 — Build the three-layer access model

**Objective:** Compose entitlements into access profiles into roles.

```bash
python3 - <<'EOF'
entitlements = {
  "AD:FIN-GL-RW":   "General ledger read/write (AD group)",
  "AD:FIN-AP-RO":   "Accounts payable read-only (AD group)",
  "AD:Domain Users":"Baseline domain access",
  "SF:Sales-Read":  "Salesforce read",
  "SF:Sales-Admin": "Salesforce administration",
}
access_profiles = {
  "General Ledger - RW":  ["AD:FIN-GL-RW"],
  "Accounts Payable - RO":["AD:FIN-AP-RO"],
  "Baseline Access":      ["AD:Domain Users"],
  "Salesforce - Read":    ["SF:Sales-Read"],
}
roles = {
  "Employee (birthright)": ["Baseline Access"],
  "Financial Analyst":     ["Baseline Access","General Ledger - RW","Accounts Payable - RO"],
  "Sales Rep":             ["Baseline Access","Salesforce - Read"],
}
for role, profiles in roles.items():
    granted = [e for p in profiles for e in access_profiles[p]]
    print(f"\nROLE: {role}")
    for p in profiles:
        print(f"  profile: {p}")
    print(f"  -> grants {len(granted)} entitlements: {granted}")
print("\nA manager approves 'Financial Analyst' — a job — not five raw AD group DNs.")
EOF
```

**Expected result:** Each role resolves down through access profiles to concrete entitlements. The final line is the whole point: the model lets a manager approve a **job**, while the system still knows exactly which technical entitlements that implies. This layering — entitlement → access profile → role — is the ISC access model the Administrator and Engineer exams both test.

**Negative test:** Presenting raw entitlements for approval — reviewers rubber-stamp what they cannot interpret, and the access review becomes a compliance ritual that catches nothing.

**Cleanup:** None.

### Lab 3.2 — Birthright roles by attribute (RBAC + ABAC)

**Objective:** Assign access automatically from identity attributes.

```bash
python3 - <<'EOF'
def assigned_roles(identity):
    roles = ["Employee (birthright)"]                       # everyone
    if identity["dept"] == "Finance":  roles.append("Financial Analyst")
    if identity["dept"] == "Sales":    roles.append("Sales Rep")
    if identity["type"] == "Contractor" and "Financial Analyst" in roles:
        roles.remove("Financial Analyst")                   # contractors: no GL write
        roles.append("Finance Read-Only (contractor)")
    return roles

people = [
  {"name":"Jane Doe","dept":"Finance","type":"Employee"},
  {"name":"Sam Lee","dept":"Sales","type":"Employee"},
  {"name":"Kim Ray","dept":"Finance","type":"Contractor"},
]
for p in people:
    print(f"{p['name']:10} ({p['type']:10} {p['dept']:8}) -> {assigned_roles(p)}")
print("\nBirthright access needs no request/approval — it is granted by WHO YOU ARE (attributes).")
EOF
```

**Expected result:** Everyone gets the birthright Employee role; department drives the job role; and the contractor is deliberately downgraded to read-only. Attribute-driven assignment (**ABAC** membership criteria) selecting **RBAC** roles is how real deployments combine the two — automatic, consistent, and still reviewable because the outcome is a named role.

**Negative test:** Making all access request-based including birthright — every new hire waits on approvals for the intranet, so the service desk drowns and managers approve reflexively.

**Cleanup:** None.

### Lab 3.3 — Mine roles and detect role explosion

**Objective:** Derive candidate roles from real entitlement data, then check model quality.

```bash
python3 - <<'EOF'
from collections import Counter
# Observed: what people in each department actually hold
observed = [
  ("Finance", frozenset({"GL-RW","AP-RO","Baseline"})),
  ("Finance", frozenset({"GL-RW","AP-RO","Baseline"})),
  ("Finance", frozenset({"GL-RW","AP-RO","Baseline","Treasury-RW"})),   # one outlier
  ("Sales",   frozenset({"CRM-Read","Baseline"})),
  ("Sales",   frozenset({"CRM-Read","Baseline"})),
]
by_dept = {}
for dept, held in observed:
    by_dept.setdefault(dept, []).append(held)

print("=== ROLE MINING ===")
for dept, sets in by_dept.items():
    common = set.intersection(*[set(s) for s in sets])       # the stable core
    print(f"{dept}: candidate role = {sorted(common)}  (from {len(sets)} identities)")
    for s in sets:
        extra = set(s) - common
        if extra: print(f"    exception to handle separately: {sorted(extra)}")

print("\n=== MODEL QUALITY ===")
roles_per_identity, identities, roles_defined = 3.0, 100, 400
single_member = 180
print(f"identities={identities}, roles={roles_defined}, single-member roles={single_member}")
print("VERDICT: ROLE EXPLOSION — more roles than identities and 45% single-member;" )
print("the model is no longer reviewable. Fix: model the common core, make exceptions time-bound.")
EOF
```

**Expected result:** Role mining finds the stable **common core** per department (the intersection) and surfaces the Treasury outlier as an exception rather than folding it into the role. The quality check then names the pathology: 400 roles for 100 identities with 45% single-member is **role explosion**. Mining from observed data is how you build a model that reflects reality; measuring it is how you keep it from rotting.

**Negative test:** Mining with the *union* instead of the intersection — every outlier's access lands in the base role and you over-entitle the whole department, the opposite of least privilege.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] Entitlement → access profile → role layering built and understood.
- [ ] RBAC and ABAC compared; birthright roles assigned by attribute.
- [ ] Roles mined from observed entitlement data using the common core.
- [ ] Role explosion diagnosed and its remedy stated.
