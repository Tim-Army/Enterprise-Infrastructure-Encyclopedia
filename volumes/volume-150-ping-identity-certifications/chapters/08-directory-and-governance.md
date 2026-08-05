# Chapter 08: Directory and Governance

## Learning Objectives

- Explain the directory's role as the store of identities.
- Understand identity governance — who *should* have access.
- Place access certification and the joiner-mover-leaver lifecycle.
- Recognize governance as the "should" that complements access management's "can".

*Cert relevance: PingDirectory and PingOne Identity Governance are the **directory** and **governance** certifications.*

## The directory

Underneath all of identity is the **directory** — the authoritative store of *who exists*: users, their attributes (name, email, department, group memberships), and often credentials. **PingDirectory** (and the ForgeRock-heritage **PingDS**) is Ping's high-performance directory, speaking **LDAP** and built for the scale CIAM demands — hundreds of millions of identities with millisecond lookups and high availability.

The directory is foundational because **every identity operation reads it**: authentication verifies against it, authorization reads group memberships from it, federation pulls attributes from it. A slow or unavailable directory means slow or failed logins everywhere. PingDirectory's job is to be **fast, scalable, and always available** — the reliable substrate the rest of the stack queries. The lab touches directory scale within the governance exercise.

## Identity governance

Access management ([Chapter 4](04-access-management-pingaccess-and-pingam.md)) enforces what a user *can* access. **Identity governance** answers the different, harder question: what a user *should* access — and proves it. **PingOne Identity Governance** (a ForgeRock-heritage capability) covers the **governance** discipline — the same territory the [SailPoint volume (CXXXII)](../../volume-132-sailpoint-certifications/README.md) owns deeply:

- **Access certification** — periodic reviews where managers *re-attest* that their reports still need the access they have, revoking what is no longer justified.
- **The joiner-mover-leaver lifecycle** — provisioning access when someone joins, adjusting it when they change roles (and *removing the old* access), and fully deprovisioning when they leave.
- **Segregation of duties (SoD)** — preventing toxic access combinations (the person who *creates* vendors should not also *approve payments* to them).

Governance exists because access **accumulates**: people change roles and keep old permissions ("privilege creep"), and without periodic certification, users end up with far more access than they need — a standing risk. The lab models access certification and privilege creep.

## "Can" versus "should"

The clean distinction to hold:

- **Access management (PingAccess/PingAM)** — *can* this user access this now? (Real-time enforcement.)
- **Identity governance (PingOne Identity Governance)** — *should* this user have this access at all? (Periodic review and lifecycle.)

They are complementary: enforcement without governance means correctly-enforced *excessive* access; governance without enforcement means good intentions no system applies. A complete identity program needs both — the same **least-privilege, reviewed-over-time** discipline the [CIEM (CXLVII)](../../volume-147-wiz-certifications/chapters/05-ciem-and-dspm-identity-and-data.md) and [SailPoint (CXXXII)](../../volume-132-sailpoint-certifications/README.md) volumes teach. The lab makes the "should" concrete.

## Hands-On Lab

Python models governance. **Cost:** none.

### Lab 8.1 — Access certification catches privilege creep

**Objective:** Review accumulated access and revoke what is no longer justified.

```bash
python3 - <<'EOF'
# users who have changed roles over time, accumulating access
USERS = {
  "alice": {"current_role": "engineer",
            "access": ["git", "ci-cd", "prod-db-read", "finance-portal", "old-admin-panel"]},
  "bob":   {"current_role": "sales",
            "access": ["crm", "email", "prod-db-read"]},   # why does sales have prod-db?
}
# what each role SHOULD have
ROLE_ACCESS = {
  "engineer": {"git", "ci-cd", "prod-db-read"},
  "sales":    {"crm", "email"},
}
print("ACCESS CERTIFICATION — manager reviews each user's access vs their role:\n")
total_revoked = 0
for user, info in USERS.items():
    role = info["current_role"]
    should = ROLE_ACCESS[role]
    have = set(info["access"])
    justified = have & should
    unjustified = have - should
    total_revoked += len(unjustified)
    print(f"   {user} (now: {role})")
    print(f"      justified (keep):   {sorted(justified)}")
    print(f"      NOT justified -> REVOKE: {sorted(unjustified)}")
    for a in sorted(unjustified):
        print(f"         - {a}: leftover from a past role / never cleaned up (privilege creep)")
    print()
print(f"total access revoked by this certification: {total_revoked}")
print("\nWhat certification catches:")
print("  alice — an engineer, but still holds 'finance-portal' + 'old-admin-panel' from")
print("     a previous role. Nobody removed them when she moved. PRIVILEGE CREEP.")
print("  bob — in sales, but has 'prod-db-read'. Why? Nobody knows — revoke it.")
print("\nAccess ACCUMULATES: people change roles and KEEP old permissions, because")
print("granting is eager and revoking is forgotten. Over time everyone has far more")
print("access than they need — a standing breach risk (a compromised account can reach")
print("all of it). Periodic CERTIFICATION forces a manager to re-attest 'does this")
print("person still need this?' and revoke what's stale. This is the 'SHOULD' question")
print("governance answers — separate from access management's real-time 'CAN'. Same")
print("least-privilege-over-time discipline as SailPoint IGA (CXXXII) and Wiz CIEM.")
EOF
```

**Expected result:** Access certification flagging an engineer's leftover finance and admin access and a salesperson's unexplained prod-db access as privilege creep to revoke, keeping only role-justified access. The governance lesson is that access accumulates as people change roles and keep old permissions, so periodic certification forces re-attestation and revokes the stale access that enforcement alone would keep correctly granting.

**Negative test:** Relying on access management alone to control access. It correctly enforces whatever access exists — including the excessive, crept access nobody reviewed; only governance's periodic certification asks whether the access *should* exist and removes it.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] The directory (PingDirectory / PingDS) understood as the authoritative, high-scale, always-available store of identities.
- [ ] Identity governance understood — access certification, joiner-mover-leaver lifecycle, and segregation of duties.
- [ ] Privilege creep recognized as why governance exists — access accumulates without periodic review.
- [ ] Governance ("should") distinguished from access management ("can") as complementary halves of a complete program.
