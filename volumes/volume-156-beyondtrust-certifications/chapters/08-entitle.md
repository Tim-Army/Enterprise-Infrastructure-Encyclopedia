# Chapter 08: Entitle — Cloud and SaaS Just-in-Time Access

## Learning Objectives

- Explain Entitle and just-in-time (JIT) access for cloud and SaaS.
- Describe self-service access requests with automated approval workflows.
- Understand JIT grants that auto-expire — least privilege for cloud entitlements.
- Recognize Entitle as BeyondTrust's cloud-permissions/modern-PAM piece.

*Cert relevance: Entitle is a Certified Administrator product — BeyondTrust's cloud/SaaS just-in-time access management.*

## What Entitle is

**Entitle** (acquired by BeyondTrust in 2024) brings PAM's principles to **cloud and SaaS**: it is a **just-in-time (JIT) access** and **entitlement management** platform for the modern, cloud-first enterprise. Where the earlier chapters secure privileged access to *infrastructure*, Entitle governs access to **cloud services and SaaS applications** — AWS/Azure/GCP roles, SaaS admin rights, database permissions, and the sprawling web of cloud **entitlements** that accumulate as organizations adopt more services. Its core move is **JIT**: rather than granting standing access to cloud resources, Entitle grants it **on demand, for a bounded time, then automatically revokes it.** The lab models JIT for cloud.

## Self-service requests with automated workflows

Entitle's mechanism is **self-service access requests** with **automated approval workflows.** When someone needs access to a cloud resource or SaaS app, they **request it** (often through a chat tool or portal); the request routes through a **policy-driven approval workflow** (the right approver, automatically), and on approval the access is **granted immediately and automatically** — no ticket queue, no manual IAM change, no admin bottleneck. This makes least privilege **practical**: the reason organizations over-grant standing access is that just-in-time access is otherwise slow and painful. Entitle removes the friction, so the secure path is also the *easy* path. The lab models the request workflow.

## JIT grants that auto-expire

The security payoff is **auto-expiry**: an Entitle grant is **time-bounded** and **revoked automatically** when it expires. Access that is only needed for a task lives only for that task; nothing lingers. This directly attacks **standing cloud privilege** — the over-provisioned roles and never-revoked permissions that dominate cloud risk (and that [cloud CIEM — Sysdig CLV, Wiz CXLVII](../../volume-155-sysdig-certifications/chapters/07-posture-permissions-and-compliance.md) *detect*). Entitle *prevents* the accumulation in the first place by making access ephemeral by default. It also produces a clean **audit trail** — every grant tied to a request, an approval, and an expiry — which is exactly what access reviews and compliance need. The lab models auto-expiry.

## Entitle as modern PAM

Entitle represents **PAM's evolution to the cloud.** Classic PAM secured privileged access to servers and infrastructure; Entitle extends the same principles — least privilege, JIT, no standing privilege, full auditability — to the **cloud and SaaS entitlements** that are now where much of the risk lives. It sits alongside **identity governance** ([SailPoint CXXXII](../../volume-132-sailpoint-certifications/README.md)) and **cloud-permission visibility** (CIEM), completing BeyondTrust's coverage from the endpoint to the cloud. The lab synthesizes.

## Hands-On Lab

Python models cloud JIT access. **Cost:** none.

### Lab 8.1 — Self-service JIT access with auto-expiry

**Objective:** See a request-approve-grant-expire cycle for cloud access.

```bash
python3 - <<'EOF'
import datetime
# Entitle: self-service request -> policy approval -> time-bounded grant -> auto-revoke
class Entitle:
    def __init__(self): self.grants = {}
    def request(self, user, resource, hours, approver_ok):
        if not approver_ok:
            return f"{user} -> {resource}: DENIED by policy workflow"
        expiry = datetime.datetime(2026,8,5,12,0) + datetime.timedelta(hours=hours)
        self.grants[(user, resource)] = expiry
        return f"{user} -> {resource}: GRANTED, auto-expires {expiry:%H:%M} ({hours}h)"
    def access_check(self, user, resource, now):
        exp = self.grants.get((user, resource))
        if exp is None: return "no grant (default: NO standing access)"
        if now > exp:
            del self.grants[(user, resource)]
            return "EXPIRED -> access auto-revoked (nothing lingers)"
        return "active grant"

e = Entitle()
noon = datetime.datetime(2026,8,5,12,0)
print("Cloud/SaaS just-in-time access via Entitle:\n")
print("  ", e.request("dev-anna", "aws-prod-admin", hours=2, approver_ok=True))
print("  ", e.request("dev-bob",  "aws-prod-admin", hours=2, approver_ok=False))
print()
print("   anna at 13:00 (within window):", e.access_check("dev-anna","aws-prod-admin", noon+datetime.timedelta(hours=1)))
print("   anna at 15:00 (after expiry): ", e.access_check("dev-anna","aws-prod-admin", noon+datetime.timedelta(hours=3)))
print("   anna next week (no grant):    ", e.access_check("dev-anna","aws-prod-admin", noon+datetime.timedelta(days=7)))
print("\nEntitle brings PAM to CLOUD/SaaS: default = NO standing access. Need it? SELF-SERVICE")
print("request -> automated POLICY approval -> immediate, TIME-BOUNDED grant -> AUTO-EXPIRE.")
print("This makes least privilege PRACTICAL: orgs over-grant standing access because JIT is")
print("otherwise slow; Entitle removes the friction so the secure path is the EASY path. It")
print("PREVENTS the standing-cloud-privilege accumulation that CIEM (Sysdig CLV/Wiz CXLVII)")
print("only DETECTS — and every grant carries a request+approval+expiry audit trail.")
EOF
```

**Expected result:** Anna's two-hour grant to `aws-prod-admin` is approved and auto-expires, Bob's is denied by policy, and Anna's access is active within the window but auto-revoked after expiry and absent the following week. The Entitle lesson is that cloud/SaaS access defaults to none and is granted just-in-time through self-service requests and automated approval, then auto-expires — making least privilege practical and preventing the standing-cloud-privilege accumulation that CIEM only detects.

**Negative test:** Granting standing cloud/SaaS admin roles because requesting access each time is slow. Standing cloud privilege is the dominant cloud risk; Entitle removes the friction with self-service JIT and auto-expiry, so access exists only for the task.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] Entitle understood — just-in-time access and entitlement management for cloud and SaaS.
- [ ] Self-service requests with automated approval workflows understood — least privilege made practical.
- [ ] Auto-expiring JIT grants understood — preventing standing cloud privilege, with a clean audit trail.
- [ ] Entitle recognized as PAM's evolution to the cloud, alongside governance (SailPoint) and CIEM.
