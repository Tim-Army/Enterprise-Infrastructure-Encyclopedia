# Chapter 09: Choosing Your Ping Path

## Learning Objectives

- Sequence a Ping certification path by the products you operate.
- Understand currency for product-specific certifications.
- Place Ping skills in the identity-and-access-management career.
- Assemble the volume into a study and career plan.

*Cert relevance: this chapter is the meta-guide — how to navigate the product-specific program [Chapter 1](01-the-ping-identity-certification-program.md) laid out.*

## Sequencing your path

Because the program is [product-specific](01-the-ping-identity-certification-program.md), the path follows **the products your organization runs** — you certify on what you operate, then deepen:

| Your environment | Start | Then |
|:---|:---|:---|
| **Federation / SSO shop** | Certified Professional – PingFederate | + PingAccess (access) → Advanced Administrator |
| **Cloud-first** | Certified Professional – PingOne | + PingOne DaVinci (orchestration) |
| **ForgeRock heritage** | PingOne Advanced Identity Cloud | + PingAM, PingOne Identity Governance |
| **Full-stack identity engineer** | PingFederate + PingOne | + PingAccess + DaVinci + Directory |

**PingFederate is the classic anchor** — federation is Ping's deepest strength and the most transferable IAM skill, so the PingFederate certification is the highest-value single credential for most. From there, add the products in your stack: PingAccess for access management, PingOne for cloud, DaVinci for orchestration, PingDirectory for the directory, Identity Governance for the "should."

Because the certs are product-specific, **breadth across the products you run beats depth in one you do not** — a shop running PingFederate + PingAccess + PingDirectory benefits from certifications in all three. And the **Advanced Administrator / Expert** tiers deepen the products you have already mastered.

## Currency

Ping certifications track **product versions**, which evolve — and the post-merger portfolio is evolving fast as ForgeRock products are integrated and rebranded. Treat currency as **following the product**: when your PingFederate or PingOne platform gets a major upgrade, your knowledge (and eventually your certification) needs refreshing. Ping's published exam mechanics and Certification Guide make it easy to see when an exam has been updated.

The renewal discipline is the identity-specific version of the shelf-wide rule: the platform moving under a cert is why it ages. Pair certification with hands-on operation of the products and Ping Identity Training's updated pathways, and treat each major product release as the drumbeat.

## The identity-and-access-management career

Ping skills sit at the center of enterprise security: **identity is the control plane** ([Chapter 2](02-identity-and-access-management-fundamentals.md)), and federation/access management is its backbone. An engineer who can stand up SSO, federate to SaaS and partners, enforce access policy, add MFA and adaptive auth, orchestrate journeys, and govern access is exactly the IAM profile in demand — and Ping's depth in federation makes it a strong specialty.

The career pairs naturally with the rest of the identity shelf:

- **[Okta (LXXVI)](../../volume-076-okta-certifications/README.md)** — the cloud-first IDaaS; many shops know both, and the federation concepts transfer.
- **[SailPoint (CXXXII)](../../volume-132-sailpoint-certifications/README.md)** — deep identity governance (IGA); complements Ping's access focus with the "should."
- **[CyberArk / PAM]** — privileged access management; the high-value-account layer above general IAM.
- **[Wiz (CXLVII)](../../volume-147-wiz-certifications/README.md) CIEM** — cloud entitlements; the same effective-permission discipline in the cloud.

Together — **Okta (IDaaS), Ping (federation/access), SailPoint (governance), CyberArk (PAM)** — these are the pillars of enterprise identity, and Ping is the federation-and-access specialty. The lab assembles your plan.

## Hands-On Lab

Python assembles a personal Ping plan. **Cost:** none.

### Lab 9.1 — Build your Ping certification path

**Objective:** Generate a path from the products you operate.

```bash
python3 - <<'EOF'
PATHS = {
  "federation / SSO shop": [
    ("Certified Professional - PingFederate", "the anchor — federation/SAML/OIDC/OAuth"),
    ("Certified Professional - PingAccess",   "access management (the 'can')"),
    ("PingFederate Advanced Administrator",   "deepen the flagship"),
  ],
  "cloud-first": [
    ("Certified Professional - PingOne",        "cloud SSO + MFA (75% pass mark)"),
    ("Certified Professional - PingOne DaVinci", "identity orchestration flows"),
    ("Certified Professional - PingOne Identity Governance", "the 'should'"),
  ],
  "ForgeRock heritage": [
    ("Certified Professional - PingOne Advanced Identity Cloud", "the ex-ForgeRock IAM SaaS"),
    ("Certified Professional - PingAM",  "access management (ForgeRock heritage)"),
    ("Certified Professional - PingOne Identity Governance", "governance"),
  ],
}
env = "federation / SSO shop"   # change to taste
print(f"Ping path for a: {env}\n")
print("   (all ~$395, proctored, MC, ~70Q/90min — Ping publishes the mechanics)\n")
for i, (cert, why) in enumerate(PATHS[env], 1):
    print(f"   {i}. {cert:52} {why}")
print("\nGuidance:")
print("  - certify for the PRODUCTS YOU OPERATE — it's a product-specific program.")
print("  - PingFederate is the classic ANCHOR: federation is Ping's deepest strength")
print("    and the most transferable IAM skill.")
print("  - breadth across your stack (Federate + Access + Directory) beats depth in a")
print("    product you don't run; Advanced Administrator/Expert deepen what you've")
print("    mastered.")
print("  - CURRENCY = follow the product: a major platform upgrade means refresh your")
print("    knowledge (and eventually re-certify). Ping publishes when exams update.")
EOF
```

**Expected result:** A path built from the products the organization operates, anchored on PingFederate for a federation shop (or PingOne for cloud-first, Advanced Identity Cloud for ForgeRock heritage), deepening with the adjacent products and Advanced tiers. The build-your-path lesson is that a product-specific program means certifying for what you run — breadth across your stack over depth in a product you do not operate, with currency meaning following the product's releases.

**Negative test:** Chasing a Ping certification for a product your organization does not run. The program is product-specific; certify on the products in your actual identity architecture, and let breadth across those beat an unused credential.

**Cleanup:** None.

### Lab 9.2 — Position Ping in the identity career

**Objective:** Map Ping skills to the identity pillars.

```bash
python3 - <<'EOF'
PILLARS = [
  ("Ping (federation/access)", "SSO, federation, access mgmt, MFA, orchestration", "the specialty itself"),
  ("Okta (IDaaS)",             "cloud-first identity",                    "the generalist; concepts transfer"),
  ("SailPoint (IGA)",          "identity governance — the 'should'",      "complements Ping's 'can'"),
  ("CyberArk (PAM)",           "privileged access",                       "the high-value-account layer"),
  ("Wiz CIEM (CXLVII)",        "cloud entitlements",                      "effective permissions in the cloud"),
]
print("Ping in the enterprise identity skill map:\n")
print(f"   {'skill':26}{'domain':46}why it pairs")
for skill, domain, why in PILLARS:
    print(f"   {skill:26}{domain:46}{why}")
print("\nThe career thesis: IDENTITY IS THE CONTROL PLANE. In a perimeter-less world")
print("(cloud, SaaS, remote), who you are and what you can access IS the security")
print("boundary — and federation/access management is its backbone. That's Ping's turf.")
print("\nThe rounded identity engineer combines the FOUR PILLARS:")
print("  IDaaS      (Okta)      — cloud-first SSO for the masses")
print("  FEDERATION (Ping)      — enterprise SSO, access mgmt, MFA, orchestration")
print("  GOVERNANCE (SailPoint) — who SHOULD have access (certify, lifecycle, SoD)")
print("  PAM        (CyberArk)  — privileged/admin accounts, the crown-jewel access")
print("\nNone stands alone — enforcement (Ping) needs governance (SailPoint) needs a")
print("directory needs MFA. Ping is the FEDERATION + ACCESS specialty, deepest where")
print("enterprises federate to SaaS and partners. Anchor on PingFederate, add your")
print("stack, and pair with the other pillars — that's an identity career, not just a")
print("certificate.")
EOF
```

**Expected result:** Ping skills mapped to the identity pillars — Okta (IDaaS), SailPoint (governance), CyberArk (PAM), and Wiz CIEM (cloud entitlements) — with Ping as the federation-and-access specialty. The career-positioning lesson closes the volume: identity is the control plane, Ping owns federation and access management, and it pairs with the IDaaS, governance, PAM, and cloud-entitlement skills the rest of the identity shelf teaches.

**Negative test:** Treating Ping federation as a self-contained skill. It enforces access that governance (SailPoint) should review, reads a directory, and issues MFA — the identity pillars interlock, and isolating one undersells both the platform and the career.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] A Ping path sequenced by the products you operate, anchored on PingFederate for most, with breadth across your stack.
- [ ] Currency understood for product-specific certifications — follow the product's releases, especially post-merger.
- [ ] Ping positioned in the identity career alongside Okta, SailPoint, CyberArk, and cloud CIEM.
- [ ] The volume assembled into a personal study and career plan — authenticate, federate, authorize, orchestrate, govern.
