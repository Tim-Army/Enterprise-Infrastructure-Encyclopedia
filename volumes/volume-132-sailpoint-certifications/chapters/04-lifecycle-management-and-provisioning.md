# Chapter 04: Identity Lifecycle Management and Provisioning

## Learning Objectives

- Implement the joiner-mover-leaver (JML) lifecycle with lifecycle states.
- Distinguish automatic (birthright) provisioning from requested access.
- Explain provisioning modes and why deprovisioning is the security-critical half.
- Model access accumulation ("privilege creep") and the mover event that prevents it.

## The lifecycle is the product

**Identity and Lifecycle Management** and **Provisioning** are named domains on both Identity Security Cloud certifications, and they are what an IGA platform *does* day to day: react to life events by granting and revoking access without a human retyping anything.

| Event | Trigger | Expected action |
|:---|:---|:---|
| **Joiner** | New record in the authoritative source | Create identity, assign birthright roles, provision accounts |
| **Mover** | Department/manager/job change | Grant new-role access **and revoke the old** |
| **Leaver** | Termination in HR | Disable/delete accounts, revoke all access, preserve evidence |

**Lifecycle states** (active, inactive/leave, terminated) are the mechanism: each state maps to a provisioning outcome, so the platform reacts to a *state change* rather than to a ticket.

The security asymmetry is worth stating plainly: **the joiner half fails loudly, the leaver half fails silently.** If a new hire lacks access, they complain within the hour. If a leaver keeps access, nobody notices — until it is used. That is why the leaver process and the orphan report of Chapter 02 are the audit priorities.

## Automatic vs requested access

| Path | How access is granted | Example |
|:---|:---|:---|
| **Birthright / automatic** | Role assignment by attribute, no request | Every employee gets email and the intranet |
| **Requested** | User requests → approval workflow → provisioning | Access to the general ledger |

Both end in the same provisioning action; they differ in who decides. Requested access carries an **approval chain** (manager, then access owner) and is what a certification campaign later re-examines.

## Privilege creep

The mover event is where most organizations quietly fail. When someone moves from Finance to Sales, the new access is granted (they ask for it) but the old access is often left in place (nobody asks to remove it). Over a career, access accumulates — **privilege creep** — until long-tenured employees hold more access than anyone intends and least privilege is fiction. The fix is structural: the mover event must **revoke** the roles that no longer apply, not merely add new ones.

## Hands-On Lab

Python models the lifecycle engine. **Cost:** none.

### Lab 4.1 — The joiner-mover-leaver state machine

**Objective:** Build the lifecycle engine that drives provisioning.

```bash
python3 - <<'EOF'
BIRTHRIGHT = ["Baseline Access"]
DEPT_ROLES = {"Finance":["Financial Analyst"], "Sales":["Sales Rep"], "IT":["IT Support"]}

def target_access(identity):
    """What access SHOULD this identity have right now?"""
    if identity["state"] == "terminated":
        return []                                    # leaver: nothing
    if identity["state"] == "inactive":
        return []                                    # leave of absence: suspend access
    return BIRTHRIGHT + DEPT_ROLES.get(identity["dept"], [])

def reconcile(current, target):
    grant  = [r for r in target  if r not in current]
    revoke = [r for r in current if r not in target]
    return grant, revoke

# JOINER
jane = {"name":"Jane","dept":"Finance","state":"active"}
current = []
g, r = reconcile(current, target_access(jane))
print(f"JOINER  {jane['name']}: grant={g} revoke={r}")
current = target_access(jane)

# MOVER — Finance to Sales
jane["dept"] = "Sales"
g, r = reconcile(current, target_access(jane))
print(f"MOVER   {jane['name']}: grant={g} revoke={r}   <-- revoking the OLD role is the critical half")
current = target_access(jane)

# LEAVER
jane["state"] = "terminated"
g, r = reconcile(current, target_access(jane))
print(f"LEAVER  {jane['name']}: grant={g} revoke={r}")
EOF
```

**Expected result:** The joiner gains baseline plus Financial Analyst; the **mover grants Sales Rep and revokes Financial Analyst**; the leaver has everything revoked. The `reconcile` function is the engine's essence — compute the target state from attributes, diff it against current access, and emit grants and revokes. Reconciling to a *target state* (rather than processing ad-hoc requests) is what makes the outcome deterministic and auditable.

**Negative test:** A mover implementation that only grants — Jane accumulates Financial Analyst *and* Sales Rep, which is both a least-privilege failure and, if those roles conflict, a separation-of-duties violation (Chapter 05).

**Cleanup:** None.

### Lab 4.2 — Requested access with an approval chain

**Objective:** Model the request-approval-provision path.

```bash
python3 - <<'EOF'
def request_access(requester, item, manager_approves, owner_approves, sod_clean):
    trail = [f"REQUEST: {requester} -> {item}"]
    if not manager_approves:
        trail.append("DENIED at manager approval"); return trail, False
    trail.append("manager approved")
    if not sod_clean:
        trail.append("BLOCKED: separation-of-duties violation"); return trail, False
    if not owner_approves:
        trail.append("DENIED by access owner"); return trail, False
    trail.append("access owner approved")
    trail.append("PROVISIONED (and recorded for the next certification campaign)")
    return trail, True

for case in [("Jane","General Ledger - RW",True,True,True),
             ("Sam","Payments - Approve",True,True,False),
             ("Kim","Salesforce - Admin",False,True,True)]:
    trail, ok = request_access(*case)
    print(f"\n{case[0]} requesting {case[1]}: {'GRANTED' if ok else 'NOT GRANTED'}")
    for step in trail: print(f"   {step}")
EOF
```

**Expected result:** Jane's clean request provisions; Sam's is blocked by a **separation-of-duties** check before any approval can override it; Kim's dies at manager approval. Note the ordering — the SoD policy check sits *between* approvals, because a policy violation is not something a manager should be able to approve away casually. Every step is recorded, which is what makes the later access review meaningful.

**Negative test:** Provisioning first and checking policy later ("we'll catch it in the next campaign") — the violation is live for months, and the campaign becomes a cleanup queue instead of a control.

**Cleanup:** None.

### Lab 4.3 — Privilege creep over a career

**Objective:** Quantify what happens when the mover event does not revoke.

```bash
python3 - <<'EOF'
moves = [("Helpdesk",["IT Support"]), ("Finance",["Financial Analyst"]),
         ("Treasury",["Treasury Ops"]), ("Sales",["Sales Rep"])]

naive, correct = set(["Baseline"]), set(["Baseline"])
for dept, roles in moves:
    naive |= set(roles)                       # grants only
    correct = {"Baseline"} | set(roles)       # reconcile to target state
    print(f"after move to {dept:10}: naive={sorted(naive)}")
    print(f"{'':22} correct={sorted(correct)}")
print(f"\nAfter 4 moves: naive holds {len(naive)} roles, correct holds {len(correct)}.")
print("The naive employee can now raise a purchase order, approve it, and pay it.")
EOF
```

**Expected result:** The grant-only path accumulates five roles across a career while the reconciling path always holds exactly what the current job needs. The last line names the real consequence: accumulated access across Finance, Treasury, and Sales reconstitutes a **toxic combination** — the very thing separation-of-duties policy exists to prevent. Privilege creep is not untidiness; it is how insider fraud becomes possible.

**Negative test:** Relying on annual access reviews to undo creep — reviewers see a long-tenured employee's large access set and assume it is justified; the accumulation persists.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] JML lifecycle implemented as a reconcile-to-target-state engine.
- [ ] Birthright vs requested access distinguished, with the approval chain modeled.
- [ ] The mover revoke — the commonly missed half — implemented.
- [ ] Privilege creep quantified and linked to separation-of-duties risk.
