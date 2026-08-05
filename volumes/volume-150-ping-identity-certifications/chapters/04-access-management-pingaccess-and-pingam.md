# Chapter 04: Access Management — PingAccess and PingAM

## Learning Objectives

- Explain centralized, policy-based access management.
- Understand protecting web applications and APIs at the gateway.
- Place session management and token mediation.
- Recognize PingAccess and PingAM as the authorization enforcement layer.

*Cert relevance: PingAccess and PingAM are the **access-management** certifications — the authorization half of the portfolio.*

## Centralized access management

Where [federation (Chapter 3)](03-federation-pingfederate.md) handles *authentication*, **access management** handles *authorization enforcement* — deciding, at request time, whether *this* authenticated user may access *this* resource, and enforcing it. **PingAccess** (Ping-origin) and **PingAM** (ForgeRock-origin) are Ping's access-management products.

The key idea is **centralization**: instead of every application implementing its own access logic (inconsistently, buggily, un-auditably), access decisions are **externalized** to a central policy engine that sits in front of applications and APIs. The application no longer asks "is this user allowed?" — the access-management layer answers that *before the request reaches the app*, uniformly, from central policy. This is the [policy-as-code / centralized-authorization](../../volume-147-wiz-certifications/chapters/08-operationalizing-wiz.md) discipline applied to access.

## Protecting web apps and APIs

Access management enforces at the **gateway** — a **reverse proxy** (PingAccess) or policy agent that intercepts requests to protected resources:

- For a **web application**: the gateway checks the user has a valid session and satisfies the access policy before proxying the request through; unauthenticated users are redirected to the IdP to log in.
- For an **API**: the gateway validates the OAuth **access token** and its scopes ([Chapter 3](03-federation-pingfederate.md)) before allowing the call — rejecting requests with missing, expired, or insufficiently-scoped tokens.

This gateway model means protection is **consistent and external**: the app does not have to be modified to be secured, and policy changes apply everywhere at once. The lab models policy-based gateway decisions.

## Sessions and token mediation

Two operational concepts the exams cover:

- **Session management** — after login, the user has a **session**; access management tracks it, enforces **timeouts** (idle and absolute), and enables **single logout** (ending the session everywhere). Session handling is a security-sensitive balance: too long is a hijack risk, too short annoys users.
- **Token mediation** — the access layer can **translate** between token types at the boundary: accept a user's SSO session and mint a scoped OAuth token for the backend API, so the app never handles raw credentials. PingAccess/PingAM mediate between the front-end session and back-end tokens.

The lab focuses on the policy-decision core, which is the heart of the access-management exams.

## Hands-On Lab

Python models access-management enforcement. **Cost:** none.

### Lab 4.1 — Centralized policy-based access decisions

**Objective:** Enforce access at a central gateway from policy.

```bash
python3 - <<'EOF'
# a central access-management policy engine in front of protected resources
POLICIES = {
  # resource,          required_role,  extra_condition
  "/admin":            ("admin",       "mfa_satisfied"),
  "/reports":          ("analyst",     None),
  "/api/payments":     ("finance",     "mfa_satisfied"),
  "/public":           (None,          None),
}
REQUESTS = [
  # user,   roles,                 mfa,    resource
  ("alice", ["analyst"],           False,  "/reports"),
  ("alice", ["analyst"],           False,  "/admin"),
  ("bob",   ["admin","finance"],   False,  "/admin"),         # admin but NO mfa
  ("bob",   ["admin","finance"],   True,   "/admin"),          # admin + mfa
  ("carol", ["finance"],           True,   "/api/payments"),
  ("dave",  [],                    False,  "/public"),
]
def decide(roles, mfa, resource):
    role_req, cond = POLICIES[resource]
    if role_req and role_req not in roles:
        return "DENY (missing role)"
    if cond == "mfa_satisfied" and not mfa:
        return "DENY (step-up MFA required)"
    return "ALLOW"

print("Central access-management gateway — decisions from ONE policy set:\n")
print(f"   {'user':7}{'resource':16}{'roles':22}{'mfa':>5}   decision")
for user, roles, mfa, resource in REQUESTS:
    d = decide(roles, mfa, resource)
    print(f"   {user:7}{resource:16}{str(roles):22}{str(mfa):>5}   {d}")
print("\nRead the decisions:")
print("  alice/reports -> ALLOW (has analyst). alice/admin -> DENY (not admin).")
print("  bob/admin no-mfa -> DENY: has the admin role, but /admin requires step-up MFA.")
print("  bob/admin +mfa   -> ALLOW: role AND condition satisfied.")
print("  carol/payments   -> ALLOW (finance + mfa).")
print("\nThe access-management model: the GATEWAY decides BEFORE the request reaches the")
print("app, from CENTRAL policy — role checks AND conditions (step-up MFA for sensitive")
print("resources). The apps (/admin, /api/payments) implement NO access logic")
print("themselves; PingAccess/PingAM enforce it uniformly out front.")
print("\nWhy centralize: consistency (one policy, not per-app reinventions), auditability")
print("(one place logs every decision), and agility (change the policy once, applies")
print("everywhere). Externalizing authorization from the app is the whole point — the")
print("app trusts the gateway already checked. Same policy-as-code discipline as the")
print("cloud/security shelf, applied to access.")
EOF
```

**Expected result:** A central gateway allowing and denying requests from one policy set — role checks plus step-up-MFA conditions for sensitive resources — with the applications implementing no access logic themselves. The access-management lesson is that externalizing authorization to a central policy engine at the gateway gives consistency, auditability, and agility, enforced before the request reaches the app.

**Negative test:** Letting each application implement its own access checks. They drift inconsistent, are hard to audit, and a policy change means editing every app — centralizing at PingAccess/PingAM enforces one policy uniformly out front.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] Access management understood as centralized, policy-based authorization enforcement, distinct from authentication.
- [ ] Gateway protection of web apps (sessions) and APIs (token/scope validation) understood as external and consistent.
- [ ] Session management and token mediation placed as core operational concepts.
- [ ] PingAccess and PingAM recognized as the authorization enforcement layer, externalizing access from the app.
