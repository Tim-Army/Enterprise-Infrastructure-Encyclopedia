# Chapter 05: Cloud Organization Admin and Access

## Learning Objectives

- Explain the Atlassian cloud organization model — sites, products, and the admin hub.
- Manage users, groups, and product access at organization scale.
- Secure the org with Atlassian Guard (formerly Access): SSO, SCIM, and enforced policies.
- Distinguish product administration from organization administration.

*Cert relevance: the **Atlassian Cloud Organization Admin** certification (ACP) — the org-level tier above per-product administration.*

## Product admin versus org admin

Chapters 02–04 covered administering *a product* — Jira's schemes, Confluence's spaces. This chapter is the tier above: administering the *organization* across all products, which the **Atlassian Cloud Organization Admin** certification exists for. The distinction is real and the exam cares about it:

| | **Product admin** (Jira/Confluence) | **Organization admin** |
|:---|:---|:---|
| Scope | One product's configuration | All products, all sites, the whole tenant |
| Owns | Workflows, spaces, permission schemes | Users, security policy, billing, domains |
| Question answered | "How is this project configured?" | "Who has access to what, across everything?" |

The org admin sits above the product admins and owns the things that cross products: **identity, security, and access.** A Jira admin who cannot get an org-level setting changed is bumping into exactly this boundary.

## The cloud organization model

Atlassian's cloud hierarchy is layered:

| Level | Is |
|:---|:---|
| **Organization** | The top-level entity — your company's whole Atlassian tenant |
| **Site** | An instance (`yourcompany.atlassian.net`) hosting products; an org can have several |
| **Product** | Jira, Confluence, JSM, etc., running on a site |
| **Admin hub** | `admin.atlassian.com` — where org admins manage users, security, and billing |

The **admin hub** is the org admin's console, distinct from any single product's settings. Managing users, verifying domains, setting security policy, and controlling which users can access which products all happen here, above the products.

## Atlassian Guard

**Atlassian Guard** (formerly Atlassian Access) is the security layer for the organization, and it is where the org-admin certification gets serious:

| Capability | Does |
|:---|:---|
| **SSO (SAML/OIDC)** | Authenticate users through your identity provider, not Atlassian passwords |
| **SCIM provisioning** | Auto-create, update, and *deprovision* users from your IdP |
| **Enforced policies** | Password requirements, session duration, two-step verification, API token controls |
| **Domain verification** | Claim your domains so you can enforce policy on all users with those email addresses |

The two that matter most, and that the lab models, are **domain verification** and **SCIM deprovisioning**:

- **Domain verification is the precondition.** You can only enforce security policy on users whose email domains you have *verified and claimed*. An unverified domain means users on it are outside your policy — a real gap.
- **SCIM deprovisioning closes the offboarding hole.** Without it, a departed employee's Atlassian access lingers until someone manually removes it — the classic offboarding failure. With SCIM, disabling them in the IdP removes their Atlassian access automatically, the same lifecycle discipline as [Okta (LXXVI)](../../volume-076-okta-certifications/README.md) and [SailPoint (CXXXII)](../../volume-132-sailpoint-certifications/README.md).

## Hands-On Lab

Python models cloud org administration. **Cost:** none.

### Lab 5.1 — Domain verification is the policy precondition

**Objective:** Show which users fall outside enforced security.

```bash
python3 - <<'EOF'
VERIFIED_DOMAINS = {"acme.com", "acme.co.uk"}
USERS = [
  ("alice@acme.com",          "employee"),
  ("bob@acme.co.uk",          "employee"),
  ("carol@acme-contractor.com","contractor — DIFFERENT domain"),
  ("dave@gmail.com",          "employee who signed up with personal email"),
  ("erin@acme.com",           "employee"),
]
print(f"{'user':30}{'domain verified?':>18}   under policy?")
outside = 0
for email, role in USERS:
    domain = email.split("@")[1]
    verified = domain in VERIFIED_DOMAINS
    if not verified: outside += 1
    status = "ENFORCED (SSO, 2SV, session policy)" if verified else "*** OUTSIDE POLICY"
    print(f"{email:30}{'yes' if verified else 'NO':>18}   {status}")
print(f"\n{outside} of {len(USERS)} users are OUTSIDE enforced security policy — because")
print("Atlassian Guard can only enforce policy on VERIFIED domains you have claimed.")
print("\nThe two gaps here are both real and both common:")
print("  carol@acme-contractor.com — a legit contractor on an unclaimed domain.")
print("     SSO and 2SV do NOT apply to her; she logs in with an Atlassian password.")
print("  dave@gmail.com — an employee who signed up with a PERSONAL email. Invisible")
print("     to domain-based policy entirely.")
print("\nThe org admin's job: VERIFY every domain your people use (including")
print("subsidiary and contractor domains), and find the personal-email signups")
print("(Guard reports them) and migrate them onto a managed account. Unverified")
print("domain = a user your security policy cannot touch, which is exactly the")
print("account an attacker prefers.")
EOF
```

**Expected result:** Two of five users falling outside enforced policy — a contractor on an unclaimed domain and an employee on a personal email. Domain verification as the policy precondition is the lesson — Guard can only enforce on claimed domains, so the org admin's first security task is claiming every domain their people actually use.

**Negative test:** Enabling SSO and 2SV and assuming everyone is covered. The personal-email signups and unclaimed-domain contractors authenticate with Atlassian passwords, entirely outside the enforced policy.

**Cleanup:** None.

### Lab 5.2 — SCIM closes the offboarding hole

**Objective:** Compare manual and automated deprovisioning.

```bash
python3 - <<'EOF'
from datetime import date, timedelta
DEPARTURES = [
  ("frank", date(2026, 7, 1)),
  ("gina",  date(2026, 7, 15)),
  ("hank",  date(2026, 7, 28)),
]
today = date(2026, 8, 4)
print("Employees who left the company:\n")
print("WITHOUT SCIM (manual deprovisioning — someone must remember):")
for name, left in DEPARTURES:
    days = (today - left).days
    # manual removal is sporadic; model realistic lag
    removed = days > 20   # often only caught in a periodic access review
    status = f"access removed" if removed else f"*** STILL HAS ACCESS ({days} days after leaving)"
    print(f"   {name:6} left {left} -> {status}")
print("\nWITH SCIM (disable in IdP -> Atlassian access removed automatically):")
for name, left in DEPARTURES:
    print(f"   {name:6} left {left} -> access removed SAME DAY (IdP deprovision cascades)")
print("\nThe gap without SCIM: departed employees keep Jira/Confluence access for")
print("WEEKS — until a manual review catches them. Every one is a live credential")
print("for a person no longer employed, holding whatever they held on their last day")
print("(source code discussions, security runbooks, customer data in tickets).")
print("\nSCIM makes deprovisioning a CONSEQUENCE of the IdP action HR already takes")
print("(disabling the account), not a separate task someone must remember. This is")
print("the identity-lifecycle discipline from Okta (LXXVI) and SailPoint (CXXXII),")
print("applied to the Atlassian org: the org admin wires Atlassian into the")
print("company's joiner-mover-leaver process so access tracks employment automatically.")
EOF
```

**Expected result:** Departed employees retaining access for weeks under manual deprovisioning versus same-day removal via SCIM. The consequence-not-task framing is the security lesson — SCIM makes offboarding automatic by cascading the IdP disable that HR already performs, closing the lingering-access hole that manual processes reliably leave open.

**Negative test:** Relying on periodic access reviews to catch departed users. Between reviews, ex-employees hold live credentials to whatever they last accessed.

**Cleanup:** None.

### Lab 5.3 — Product access at org scale

**Objective:** Grant the right products to the right people without over-licensing.

```bash
python3 - <<'EOF'
GROUPS = {
  "engineering":  {"jira", "confluence", "jsm-agent"},
  "support":      {"jsm-agent", "confluence"},
  "sales":        {"confluence"},
  "everyone":     {"confluence-view"},   # everyone can read the wiki
}
USERS = {
  "alice": ["engineering", "everyone"],
  "bob":   ["support", "everyone"],
  "carol": ["sales", "everyone"],
  "dave":  ["everyone"],                  # read-only wiki user
}
PRODUCT_COST = {"jira": 8, "confluence": 6, "jsm-agent": 20, "confluence-view": 0}
print(f"{'user':8}{'products':40}{'monthly cost':>13}")
total = 0
for u, group_list in USERS.items():
    products = set()
    for g in group_list: products |= GROUPS[g]
    cost = sum(PRODUCT_COST.get(p, 0) for p in products)
    total += cost
    print(f"{u:8}{', '.join(sorted(products)):40}${cost:>11}")
print(f"\ntotal monthly product cost: ${total}")
print("\nAccess is granted by GROUP membership, and group -> product mapping is the")
print("org admin's lever. Two things this gets right:")
print("  - dave (wiki reader) costs $0 — he has confluence-VIEW, not a full seat.")
print("    Granting him a full Confluence license would be pure waste.")
print("  - jsm-AGENT ($20) goes ONLY to support and engineering who work tickets —")
print("    not to sales, who would never use it. Agent seats are the expensive ones.")
print("\nThe org admin's cost discipline: map groups to the MINIMUM products each")
print("role needs. Over-licensing (everyone gets everything) is invisible on any")
print("single account and enormous across thousands of users — the same least-")
print("privilege instinct as security, applied to the bill. Review group->product")
print("mappings periodically; roles drift and licenses accumulate.")
EOF
```

**Expected result:** Product access mapped by group with a read-only user at zero cost and expensive agent seats restricted to those who work tickets. The least-privilege-applied-to-licensing framing is the org-admin lesson — over-provisioning is invisible per-account and large at scale, so group-to-product mappings deserve the same minimization instinct as security permissions.

**Negative test:** Granting everyone every product "to keep it simple." The agent seats alone, spread across a whole company, cost more than the entire minimized allocation — for access most users never touch.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] Org administration distinguished from product administration by scope and what it owns.
- [ ] The org/site/product/admin-hub hierarchy understood.
- [ ] Atlassian Guard configured: domain verification as the policy precondition, SCIM for offboarding.
- [ ] Product access mapped by group to the minimum each role needs, reviewed periodically.
