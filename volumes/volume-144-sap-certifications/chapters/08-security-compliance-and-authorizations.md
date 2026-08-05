# Chapter 08: Security, Compliance, and Authorizations

## Learning Objectives

- Explain the SAP authorization model: roles, profiles, and authorization objects.
- Understand segregation of duties (SoD) and why it dominates SAP security audits.
- Place SAP security within GRC and the compliance obligations SAP systems carry.
- Recognize the security dimension threaded through every SAP certification.

*Cert relevance: security and authorizations appear across the S/4HANA and BTP certifications; **SAP GRC** (Governance, Risk, Compliance) and identity/authorization topics are their own specialization. This chapter is **defensive** — access control, compliance, and audit.*

## Why SAP security is its own discipline

SAP systems run the money: the general ledger, payroll, payments, procurement. That makes SAP authorization one of the highest-stakes access-control problems in any enterprise, and it has a model unlike anything else on this shelf — dense, granular, and audited constantly.

The reason it dominates audits is **segregation of duties**: the same person must not be able to both *create a vendor* and *pay that vendor*, or both *enter a purchase order* and *approve it*, because the combination enables fraud. SAP's authorization model exists largely to make and prove such separations, and every external financial audit of an SAP shop examines them.

## The authorization model

SAP access is built in layers:

| Layer | Is |
|:---|:---|
| **Authorization object** | The atomic permission check — e.g. "post to company code X" with fields for what and where |
| **Authorization** | Specific values filled into an object's fields |
| **Role** | A bundle of authorizations packaged for a job function |
| **User assignment** | Roles granted to a user |

A user's effective access is the union of their roles' authorizations, each checked against authorization objects at runtime. The model's power — and its difficulty — is the **combinatorial** nature: access is not a list of screens but a matrix of object-plus-value checks, and a dangerous capability often emerges from the *combination* of two individually-reasonable roles.

## Segregation of duties

SoD is the security concept SAP certifications and audits care about most:

- A **SoD conflict** exists when one user holds two capabilities whose combination is a fraud or error risk (create-vendor + pay-vendor; create-PO + approve-PO; maintain-bank-details + run-payments).
- **Conflicts hide in role combinations.** Each role passes review alone; the risk is the user who holds both. This is the same emergent-from-combination problem as [Chapter 04's clean-core interactions](04-btp-and-abap-cloud-development.md) and Guardicore's per-label policy — the danger is in the composition, not the parts.
- **SAP GRC Access Control** exists to detect these at scale: define the conflict ruleset, scan every user's role combination, report and remediate.

The lab models an SoD scan, because it is the canonical SAP-security exercise and the one an auditor will run against a real system.

## GRC and compliance

SAP **Governance, Risk, and Compliance (GRC)** wraps the security model with the business-control layer: access control (SoD, provisioning, emergency access), process control, and risk management. SAP systems also carry direct regulatory weight — **financial reporting controls (SOX)**, data protection (GDPR for the personal data in HR and CRM), and industry-specific obligations — because the SAP system *is* the system of record the regulations are about.

The through-line for a certification candidate: **security is not a separate SAP module you can skip if you are "just" an FI or SD consultant.** Every functional consultant designs roles, every design has SoD implications, and every go-live is audited. The security dimension is threaded through the whole program.

## Hands-On Lab

Python models SAP security. **Cost:** none. Defensive throughout.

### Lab 8.1 — A segregation-of-duties scan

**Objective:** Find fraud-enabling role combinations.

```bash
python3 - <<'EOF'
# SoD conflict rules: pairs of capabilities that must not coexist in one user
SOD_RULES = [
  ("create_vendor", "pay_vendor",        "vendor fraud: invent a payee and pay it"),
  ("create_po",     "approve_po",         "self-approved purchasing"),
  ("maintain_bank", "run_payments",       "redirect payments to own account"),
  ("post_journal",  "approve_journal",    "unreviewed GL manipulation"),
]
ROLES = {
  "AP_Clerk":       {"create_vendor", "post_invoice"},
  "AP_Manager":     {"pay_vendor", "approve_po"},
  "Buyer":          {"create_po"},
  "Treasury":       {"maintain_bank", "run_payments"},
  "GL_Accountant":  {"post_journal"},
}
USERS = {
  "alice": ["AP_Clerk"],
  "bob":   ["AP_Clerk", "AP_Manager"],        # <- create_vendor + pay_vendor
  "carol": ["Buyer", "AP_Manager"],           # <- create_po + approve_po
  "dave":  ["Treasury"],                       # <- maintain_bank + run_payments (within one role!)
  "erin":  ["GL_Accountant"],
}
def user_caps(u): 
    caps = set()
    for r in USERS[u]: caps |= ROLES[r]
    return caps
print("SoD scan across all users:\n")
findings = 0
for u in USERS:
    caps = user_caps(u)
    for a, b, risk in SOD_RULES:
        if a in caps and b in caps:
            findings += 1
            src = [r for r in USERS[u] if a in ROLES[r] or b in ROLES[r]]
            print(f"  CONFLICT: {u} holds {a} + {b}")
            print(f"            risk: {risk}")
            print(f"            from roles: {', '.join(src)}\n")
print(f"{findings} SoD conflicts found across {len(USERS)} users.")
print("\nNote WHERE they come from:")
print("  bob & carol: conflict emerges from TWO roles, each fine alone. No single")
print("     role review would catch it — only the COMBINATION scan does.")
print("  dave: conflict is WITHIN one role (Treasury bundles maintain_bank +")
print("     run_payments) — a role-design defect the scan also catches.")
print("\nThis scan IS the SAP security audit. GRC Access Control runs it continuously")
print("against a ruleset of hundreds of conflicts. The remediation is role redesign")
print("or, where the business genuinely needs the combination, a documented")
print("MITIGATING CONTROL (a compensating review) — never just silencing the finding.")
EOF
```

**Expected result:** Three SoD conflicts, two emerging from role combinations no single-role review would catch and one from a badly-designed role. The combination-versus-single-role distinction is the security lesson — the dangerous access emerges from composition, which is why a continuous cross-role scan (GRC Access Control) is the only reliable control.

**Negative test:** Reviewing roles one at a time for security. Bob's and Carol's conflicts are invisible to per-role review; they exist only in the combination.

**Cleanup:** None.

### Lab 8.2 — Mitigating controls versus removing access

**Objective:** Decide how to resolve each conflict.

```bash
python3 - <<'EOF'
CONFLICTS = [
  # user, conflict,                    business_need_for_both, alternative_staff
  ("bob",   "create_vendor+pay_vendor", "no — split is easy",   True),
  ("carol", "create_po+approve_po",     "no — separate approver exists", True),
  ("dave",  "maintain_bank+run_payments","small team, one treasury person", False),
]
print(f"{'user':6}{'conflict':30}{'resolution'}")
for u, conflict, need, alt in CONFLICTS:
    if alt:
        res = "REMOVE — reassign one capability to another person (clean fix)"
    else:
        res = "MITIGATING CONTROL — can't split (small team); add compensating review"
    print(f"{u:6}{conflict:30}{res}")
print("\nTwo legitimate resolutions, and the order of preference matters:")
print("  1. REMOVE the conflict (preferred): split the duties across people.")
print("     bob and carol have colleagues who can hold the other half — just do it.")
print("  2. MITIGATING CONTROL (when you genuinely can't split): a small treasury")
print("     team may HAVE to let one person maintain bank details and run payments.")
print("     Then you add a COMPENSATING control — e.g. an independent monthly review")
print("     of bank-detail changes against the payment run — and DOCUMENT it for audit.")
print("\nWhat is NOT a resolution: marking the finding 'accepted' with no control.")
print("That is how the fraud in the risk column actually happens. An SoD conflict is")
print("either REMOVED or MITIGATED-AND-DOCUMENTED; 'ignored' is an audit failure and")
print("a genuine exposure. The auditor will ask for the mitigating control's evidence.")
EOF
```

**Expected result:** Two conflicts removed by reassigning duties and one — unavoidable on a small team — resolved with a documented mitigating control. The order of preference is the discipline: remove where you can, mitigate-and-document where you truly cannot, and never simply accept, because the risk column is what accepting silently permits.

**Negative test:** Accepting an SoD conflict with no mitigating control because "it's a small team and we trust them." That is the exact scenario the control exists to prevent, and the auditor scores it a finding regardless of trust.

**Cleanup:** None.

### Lab 8.3 — Security is everyone's certification

**Objective:** Show the security dimension in a functional role's work.

```bash
python3 - <<'EOF'
FI_CONSULTANT_TASKS = [
  # task,                                        has_security_dimension
  ("configure the chart of accounts",            "who may post to which company code"),
  ("set up the payment program",                 "SoD: who runs payments vs maintains banks"),
  ("design AP clerk role",                        "exactly the create_vendor/pay_vendor split"),
  ("build a financial report",                    "row-level: who sees which cost centers"),
  ("set up the close process",                    "SoD: post vs approve journals"),
]
print("An FI consultant's 'functional' tasks — every one has a SECURITY dimension:\n")
for task, sec in FI_CONSULTANT_TASKS:
    print(f"   {task:38} -> {sec}")
print("\nNONE of these are 'the security team's job.' The FI consultant DESIGNS the")
print("roles, and every design decision is an SoD decision. Configure the payment")
print("program without thinking about who-runs-vs-who-maintains, and you have built")
print("the dave conflict from Lab 8.1 into the system by default.")
print("\nThis is why security threads through the WHOLE certification program rather")
print("than sitting in one exam: an FI, SD, or MM consultant who cannot reason about")
print("authorizations and SoD builds systems that fail audit. 'I'm just the")
print("functional consultant' is not available — in SAP, functional design IS")
print("security design, and the practical exams (Chapter 07) can put you in a system")
print("and ask you to build a role correctly, SoD and all.")
EOF
```

**Expected result:** Every task in an FI consultant's "functional" work carrying a security dimension, from chart-of-accounts posting rights to SoD in the payment program. The "functional design is security design" framing is the chapter's thesis — security is not a skippable specialty but a dimension of every functional role, which is why it threads through the whole program rather than living in one exam.

**Negative test:** A functional consultant treating authorizations as someone else's problem. The roles they design carry the SoD conflicts; abdicating the security dimension builds the conflicts in by default.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] The authorization model (objects, authorizations, roles, assignment) understood as combinatorial.
- [ ] Segregation of duties understood, with conflicts emerging from role combinations.
- [ ] SoD conflicts resolved by removal first, documented mitigating controls second, never ignored.
- [ ] Security recognized as a dimension of every functional role, not a separate specialty.
