# Chapter 02: Identity and Access Management Fundamentals

## Learning Objectives

- Distinguish authentication from authorization.
- Explain single sign-on and why federation exists.
- Understand workforce versus customer identity (CIAM).
- Place identity as the security control plane.

*Cert relevance: these fundamentals underlie every Ping certification — you cannot administer PingFederate or PingOne without them.*

## Authentication versus authorization

The two words that anchor all of IAM, and are constantly confused:

| | **Authentication (AuthN)** | **Authorization (AuthZ)** |
|:---|:---|:---|
| Answers | *Who are you?* | *What are you allowed to do?* |
| Verifies | Identity (password, MFA, biometric) | Permissions (roles, policies, scopes) |
| Example | Logging in proves you are Alice | Alice can read the file but not delete it |

**Authentication** establishes *identity* — proving you are who you claim. **Authorization** determines *access* — what that proven identity may do. They are sequential (authenticate first, then authorize) and distinct: a system can know exactly who you are (authenticated) and still deny you (not authorized). Ping's portfolio splits along this line — [PingFederate/PingOne](03-federation-pingfederate.md) handle authentication and federation; [PingAccess/PingAM](04-access-management-pingaccess-and-pingam.md) handle authorization. The lab makes the distinction concrete.

## Single sign-on and federation

**Single sign-on (SSO)** lets a user authenticate **once** and access many applications without logging in again to each. The user proves their identity to an **identity provider (IdP)**, which then vouches for them to each application (**service provider, SP**). No more twenty passwords for twenty apps.

**Federation** extends SSO **across organizational and domain boundaries** — letting an identity from one domain (your company's IdP) be trusted by an application in *another* domain (a SaaS vendor, a partner). This is what **PingFederate** does, using standards like **SAML** and **OIDC** ([Chapter 3](03-federation-pingfederate.md)): the SaaS app trusts your company's IdP to authenticate your employees, so they log in with their corporate identity, and the app never stores their password. Federation is the backbone of modern SSO, and Ping's deepest strength. The lab models the SSO trust flow.

## Workforce versus customer identity

IAM serves two very different populations:

- **Workforce identity** — your *employees* accessing *internal and SaaS* apps. Bounded, known, managed (onboarded/offboarded via HR). The classic IAM problem.
- **Customer identity (CIAM)** — your *customers* accessing your *public-facing* apps. Unbounded (millions), self-registering, and demanding a *frictionless* experience (a clunky login loses customers) while still being *secure*.

They pull in different directions: workforce IAM optimizes for control and governance; CIAM optimizes for scale, self-service, and user experience without sacrificing security. Ping serves **both**, and knowing which problem you are solving shapes every design choice. The lab is covered within the fundamentals exercises.

## Identity as the control plane

The unifying idea — the same one the [Okta](../../volume-076-okta-certifications/README.md), [SailPoint](../../volume-132-sailpoint-certifications/README.md), and [Wiz CIEM (CXLVII)](../../volume-147-wiz-certifications/chapters/05-ciem-and-dspm-identity-and-data.md) volumes teach — is that **identity is the security control plane.** In a world without a fixed network perimeter (cloud, SaaS, remote work), *who you are* and *what you can access* is the boundary that matters. Every access decision flows through identity, which is why IAM is foundational security and why a federation/access platform like Ping sits at the center of an enterprise's security architecture. The lab grounds this.

## Hands-On Lab

Python models IAM fundamentals. **Cost:** none.

### Lab 2.1 — Authentication is not authorization

**Objective:** See why proving identity and granting access are separate steps.

```bash
python3 - <<'EOF'
USERS = {
  "alice": {"password_ok": True,  "roles": ["reader"]},
  "bob":   {"password_ok": True,  "roles": ["reader", "admin"]},
  "mallory": {"password_ok": False, "roles": []},   # wrong password
}
RESOURCE_NEEDS = {"read_file": "reader", "delete_file": "admin"}

def authenticate(user):  return USERS[user]["password_ok"]
def authorize(user, action):
    need = RESOURCE_NEEDS[action]
    return need in USERS[user]["roles"]

print("Two SEPARATE gates: AuthN (who are you?) then AuthZ (what can you do?)\n")
for user in ["alice", "bob", "mallory"]:
    for action in ["read_file", "delete_file"]:
        authn = authenticate(user)
        if not authn:
            print(f"   {user:8} {action:12} -> AUTHENTICATION FAILED (not logged in)")
            break
        authz = authorize(user, action)
        verdict = "ALLOWED" if authz else "DENIED (authenticated, but not authorized)"
        print(f"   {user:8} {action:12} -> authN ok, authZ {'ok' if authz else 'NO'} -> {verdict}")
    print()
print("Read the key cases:")
print("  mallory  -> AUTHENTICATION fails (wrong password). Never even reaches authZ.")
print("  alice    -> authenticated, but 'delete_file' needs admin -> AUTHORIZED to read,")
print("              DENIED to delete. Known identity, insufficient permission.")
print("  bob      -> authenticated AND has admin -> allowed to delete.")
print("\nThe lesson: knowing WHO someone is (authentication) is NOT the same as what")
print("they may DO (authorization). alice is fully authenticated and still denied the")
print("delete — because authZ is a separate gate. Ping splits along this line:")
print("PingFederate/PingOne AUTHENTICATE + federate; PingAccess/PingAM AUTHORIZE.")
print("Confusing the two is the classic IAM error — 'but I logged in!' isn't access.")
EOF
```

**Expected result:** A wrong password failing authentication before authorization is even reached, and an authenticated user still denied an action their role does not permit. The AuthN-versus-AuthZ lesson is that proving who you are is a separate gate from what you may do — an authenticated identity can still be denied, and Ping's portfolio splits along exactly this line.

**Negative test:** Assuming a successful login grants access to everything. Authentication only proves identity; authorization is a separate gate, and a logged-in user is denied any action their permissions do not cover.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 2.2 — SSO and federated trust

**Objective:** Trace how one login grants access to many apps across domains.

```bash
python3 - <<'EOF'
# a user, a corporate IdP, and several apps (SPs) that trust the IdP
IDP = "corp-idp.example.com"
APPS = [
  ("email (SaaS, vendor A)",   "trusts corp-idp via SAML"),
  ("CRM (SaaS, vendor B)",     "trusts corp-idp via OIDC"),
  ("expense tool (SaaS)",      "trusts corp-idp via SAML"),
  ("internal wiki",            "trusts corp-idp via OIDC"),
]
print("WITHOUT SSO/federation (each app has its own login):")
print("   the user manages 4 separate passwords, logs in 4 times, and each SaaS")
print("   vendor STORES a copy of a corporate credential. 4 attack surfaces.\n")

print(f"WITH federation (all apps trust {IDP}):")
print("   1. user authenticates ONCE to the corporate IdP (password + MFA)")
for app, how in APPS:
    print(f"   2. opens {app:28} -> {how} -> IdP vouches -> IN, no new login")
print("\n   -> ONE authentication, access to ALL 4 apps. No app stores the password;")
print("      each just TRUSTS the IdP's assertion that 'this is a valid employee.'")
print("\nThe two wins of federation:")
print("  EXPERIENCE — one login for everything (SSO). No password sprawl.")
print("  SECURITY   — the SaaS apps NEVER see or store the corporate password; they")
print("     trust a signed assertion from the IdP. Offboard the user at the IdP once,")
print("     and access to ALL federated apps is revoked (one lifecycle).")
print("\nFederation extends this trust ACROSS domains — your IdP vouches for your")
print("employees to a THIRD-PARTY SaaS app. That cross-domain trust, via SAML/OIDC, is")
print("exactly what PingFederate does (Chapter 3), and it's the backbone of modern SSO.")
EOF
```

**Expected result:** One authentication to a corporate IdP granting access to multiple SaaS apps that trust it via SAML/OIDC, with no app storing the password. The SSO-and-federation lesson is that federated trust delivers both experience (one login) and security (apps trust a signed assertion instead of storing credentials, and offboarding at the IdP revokes all access) — the cross-domain trust PingFederate provides.

**Negative test:** Giving each SaaS app its own separate login. The user juggles many passwords and every vendor stores a copy of a corporate credential — federation replaces that with one login and a trusted assertion no app can leak.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] Authentication (who are you) distinguished from authorization (what may you do) as separate sequential gates.
- [ ] SSO and federation understood — one login across many apps, and trust extended across domains via SAML/OIDC.
- [ ] Workforce and customer identity (CIAM) distinguished by population, scale, and experience demands.
- [ ] Identity recognized as the security control plane in a perimeter-less world.
