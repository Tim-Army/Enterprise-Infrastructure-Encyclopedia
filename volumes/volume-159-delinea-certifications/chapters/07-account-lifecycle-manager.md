# Chapter 07: Account Lifecycle Manager — Governing Service Accounts

## Learning Objectives

- Explain the service-account sprawl problem.
- Describe Account Lifecycle Manager (ALM) — discovery, onboarding, governance.
- Understand the lifecycle from creation to decommission.
- Recognize service-account governance as attack-surface reduction.

*Cert relevance: Account Lifecycle Manager governs service accounts — a distinct Delinea product and a major PAM gap it closes.*

## The service-account sprawl problem

**Service accounts** — non-human accounts that applications, services, and scheduled tasks use to authenticate — are a notorious blind spot. They proliferate uncontrolled: created ad hoc for a project, given broad privileges "to make it work," their passwords set once and **never rotated** (because nobody knows what will break), and **never decommissioned** when the project ends. The result is **service-account sprawl** — hundreds or thousands of over-privileged, unmanaged, stale accounts, each a standing credential an attacker can find and abuse. Because rotating or removing one risks breaking a production dependency, they are often left untouched for years. **Account Lifecycle Manager (ALM)** exists to govern this sprawl. The lab models the problem.

## What ALM does: discovery, onboarding, governance

**Account Lifecycle Manager** brings **governance** to service accounts across their lifecycle:

- **Discovery** — find the service accounts that exist across the estate (including the forgotten ones), so you know what you actually have.
- **Onboarding** — bring discovered accounts under management: into the vault, with ownership assigned, dependencies mapped, and rotation enabled.
- **Governance** — enforce ownership, approval workflows for new accounts, periodic review, and controlled decommissioning.

The critical enabler is **dependency mapping** — knowing *what uses* a service account so its password can be rotated (and the account eventually retired) **without breaking** the services that depend on it. That is what makes governing service accounts feasible rather than paralyzing. The lab models the lifecycle.

## The service-account lifecycle

ALM manages a service account from **cradle to grave**:

1. **Request/create** — a new service account is requested through a workflow, with an **owner** and a justification, not created ad hoc.
2. **Onboard/vault** — its credential goes into the vault ([Secret Server, Ch 3](03-secret-server.md)) with rotation enabled.
3. **Operate/govern** — ownership is enforced, access is controlled, and the account is periodically reviewed for continued need and right-sized privilege.
4. **Decommission** — when no longer needed, the account is **retired** (not left as a stale standing credential).

Managing the full lifecycle prevents the sprawl from re-accumulating: every service account has an owner, a rotation schedule, and an end date. The lab models governance.

## Governance as attack-surface reduction

Governing service accounts is **attack-surface reduction**: every ungoverned, over-privileged, never-rotated service account is a standing credential attackers hunt for (they are a favorite target precisely because they are powerful and neglected). Bringing them under management — discovered, owned, vaulted, rotated, and eventually decommissioned — removes that surface. This complements [machine-secret management (Ch 6)](06-devops-secrets-and-machine-identity.md) and the [governance discipline of SailPoint (CXXXII)](../../volume-132-sailpoint-certifications/README.md): identity hygiene applied to the accounts nobody watches. The lab synthesizes.

## Hands-On Lab

Python models service-account governance. **Cost:** none.

### Lab 7.1 — Discover, map dependencies, and govern service-account sprawl

**Objective:** See ALM turn ungoverned sprawl into a managed lifecycle.

```bash
python3 - <<'EOF'
# discovered service accounts across the estate, most ungoverned
discovered = [
    {"name": "svc-sql-prod",   "managed": False, "last_rotated_days": 1400, "used_by": ["billing-app"]},
    {"name": "svc-backup",     "managed": False, "last_rotated_days": 900,  "used_by": ["backup-job"]},
    {"name": "svc-legacy-etl", "managed": False, "last_rotated_days": 2100, "used_by": []},          # orphan!
    {"name": "svc-web",        "managed": True,  "last_rotated_days": 30,   "used_by": ["web-tier"]},
]
print("Account Lifecycle Manager — discovered service accounts:\n")
ungoverned = [a for a in discovered if not a["managed"]]
print(f"   discovered: {len(discovered)}   ALREADY managed: {len(discovered)-len(ungoverned)}   UNGOVERNED: {len(ungoverned)}\n")
for a in discovered:
    stale = a["last_rotated_days"] > 365
    orphan = not a["used_by"]
    flags = []
    if not a["managed"]: flags.append("UNGOVERNED")
    if stale: flags.append(f"STALE ({a['last_rotated_days']}d since rotation)")
    if orphan: flags.append("ORPHAN (no dependencies -> DECOMMISSION)")
    print(f"   {a['name']:16} used_by={a['used_by'] or 'NONE':}  {' | '.join(flags) or 'ok (managed, fresh)'}")
print("\nGovern the lifecycle:")
print("  DISCOVER      — find them all (incl. the forgotten svc-legacy-etl).")
print("  MAP deps      — svc-sql-prod is used_by billing-app -> safe to rotate once mapped,")
print("                  WITHOUT breaking billing (the fear that leaves accounts untouched).")
print("  ONBOARD/VAULT — bring into the vault, assign an OWNER, enable ROTATION.")
print("  DECOMMISSION  — svc-legacy-etl has NO dependencies -> retire it (a pure standing risk).")
print("\nService-account sprawl = hundreds of over-privileged, never-rotated, orphaned standing")
print("credentials attackers hunt for. ALM governs cradle-to-grave (discover -> map -> vault +")
print("rotate -> decommission) so every service account has an OWNER, a rotation schedule, and")
print("an end date. Governing the accounts nobody watches = attack-surface reduction.")
EOF
```

**Expected result:** Four discovered service accounts — three ungoverned, two stale (1400/2100 days since rotation), one orphan with no dependencies flagged for decommission — turned into a managed lifecycle via discovery, dependency mapping, vaulting/rotation, and decommissioning. The ALM lesson is that service-account sprawl is a mass of over-privileged, never-rotated, orphaned standing credentials, and governing them cradle-to-grave (with dependency mapping so rotation doesn't break production) removes that neglected attack surface.

**Negative test:** Leaving service accounts unmanaged because rotating them might break something. That fear is exactly why they become stale standing risks; ALM's dependency mapping makes rotation and decommissioning safe, closing the surface instead of freezing it.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] The service-account sprawl problem understood — over-privileged, never-rotated, orphaned standing credentials.
- [ ] Account Lifecycle Manager understood — discovery, onboarding, and governance with dependency mapping.
- [ ] The service-account lifecycle understood — request, vault, govern, decommission.
- [ ] Service-account governance recognized as attack-surface reduction on the accounts nobody watches.
