# Chapter 09: Choosing Your BeyondTrust/PAM Path

## Learning Objectives

- Sequence a BeyondTrust certification path by role.
- Understand currency for a per-product, two-year-validity program.
- Place BeyondTrust/PAM skills in the identity-security career.
- Assemble the volume into a study and career plan.

*Cert relevance: this chapter is the meta-guide — how to navigate the per-product Certified Administrator program [Chapter 1](01-the-beyondtrust-program.md) laid out.*

## Sequencing your path

BeyondTrust certifies **per product** ([Chapter 1](01-the-beyondtrust-program.md)), so your path is driven by **the products you operate**:

| You are | Start with | Then add |
|:---|:---|:---|
| **PAM / IAM administrator** | Password Safe ([Ch 3](03-password-safe.md)) | PRA, EPM |
| **Endpoint / desktop engineer** | EPM for your OS ([Ch 4](04-endpoint-privilege-management.md)) | Password Safe |
| **Help desk / IT support** | Remote Support ([Ch 6](06-remote-support.md)) | PRA |
| **Cloud / platform engineer** | Entitle ([Ch 8](08-entitle.md)) | Password Safe |
| **Systems (mixed estate)** | AD Bridge ([Ch 7](07-ad-bridge.md)) | EPM Linux/Mac |

**Password Safe is the natural anchor** for most PAM roles — it is the credential-and-session core the discipline centers on. From there, certify on each product you actually run. Because the credential is per-product and validates hands-on administration, **certify on what you operate**, in the order your role touches it. The lab builds a role-based sequence.

## Currency

BeyondTrust certifications are **valid for 2 years** and renew by **purchasing new training and passing the current exam again** ([Chapter 1](01-the-beyondtrust-program.md)) — so currency is built into the program. This matters because PAM products evolve (new connectors, session controls, and — notably — the cloud expansion via Entitle), and the [threat landscape shifts under every credential](../../volume-151-sentinelone-certifications/chapters/09-choosing-your-sentinelone-path.md). Treat the two-year cycle as a genuine refresh of current product skill, not a formality, and pair it with hands-on operation. The lab covers currency.

## The identity-security career

BeyondTrust/PAM skills sit in **identity security** — one of the highest-demand areas in the field, because identity is the modern perimeter and privileged identity is its most sensitive core. A PAM engineer who understands vaulting, least privilege, session management, and JIT is exactly the profile enterprises need to defend against the credential-abuse attacks that drive most breaches. The career pairs with the adjacent identity disciplines this shelf covers:

- **[CyberArk (LXXVII)](../../volume-077-cyberark-certifications/README.md)** — the other PAM leader; knowing both is a strong PAM profile (BeyondTrust vs CyberArk is *the* comparison).
- **[SailPoint (CXXXII)](../../volume-132-sailpoint-certifications/README.md)** — identity governance (IGA); *what* access identities should have.
- **[Ping (CL)](../../volume-150-ping-identity-certifications/README.md) / [Okta (LXXVI)](../../volume-076-okta-certifications/README.md)** — access management, SSO, MFA; *who* logs in.
- **CIEM ([Sysdig CLV](../../volume-155-sysdig-certifications/README.md) / [Wiz CXLVII](../../volume-147-wiz-certifications/README.md))** — cloud entitlement visibility, adjacent to Entitle's JIT.

PAM is the privileged-access specialty within identity security. The lab positions it.

## Hands-On Lab

Python assembles a personal BeyondTrust/PAM plan. **Cost:** none.

### Lab 9.1 — Build your BeyondTrust path

**Objective:** Generate a role-appropriate, product-driven sequence.

```bash
python3 - <<'EOF'
PATHS = {
  "PAM / IAM administrator": [
    ("Password Safe", "the credential + session core of PAM (anchor)"),
    ("Privileged Remote Access", "VPN-less brokered privileged access"),
    ("Endpoint Privilege Management", "least privilege on endpoints"),
  ],
  "cloud / platform engineer": [
    ("Entitle", "cloud/SaaS just-in-time access"),
    ("Password Safe", "vaulting secrets for cloud infra"),
  ],
  "help desk / IT support": [
    ("Remote Support", "secure remote support (Bomgar)"),
    ("Privileged Remote Access", "when support needs privileged systems"),
  ],
}
role = "PAM / IAM administrator"   # change to taste
print(f"BeyondTrust Certified Administrator path for: {role}\n")
for i, (cert, why) in enumerate(PATHS[role], 1):
    print(f"   {i}. Certified Administrator — {cert:32} {why}")
print("\nGuidance:")
print("  - the credential is PER PRODUCT — certify on the products you ACTUALLY OPERATE.")
print("  - PASSWORD SAFE is the natural ANCHOR for most PAM roles (vault + sessions = the")
print("    core of the discipline); add PRA, EPM, Entitle as your role touches them.")
print("  - each cert = INSTRUCTOR-LED TRAINING + a 40Q/75% exam, valid 2 YEARS.")
print("  - CURRENCY: renew via new training + re-exam every 2 years — a real refresh as")
print("    the products evolve (esp. the cloud expansion via Entitle). Pair with hands-on.")
EOF
```

**Expected result:** A role-specific, product-driven sequence anchored on Password Safe for PAM roles (adding PRA, EPM, Entitle as the role requires). The build-your-path lesson is that BeyondTrust's per-product credential means you certify on the products you operate, Password Safe is the natural anchor for most PAM roles, and the two-year renew-by-retraining cycle keeps the skills current as the products evolve.

**Negative test:** Trying to certify on all eight products regardless of role. The credential validates hands-on administration of a specific product; certify on what you operate, anchored on Password Safe, rather than collecting badges for products you never touch.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 9.2 — Position BeyondTrust/PAM in the identity-security career

**Objective:** Map PAM skills to adjacent identity competencies.

```bash
python3 - <<'EOF'
LANDSCAPE = [
  ("PAM (BeyondTrust / CyberArk)", "secure PRIVILEGED access",       "vault, least privilege, sessions, JIT"),
  ("Access mgmt (Ping / Okta)",    "WHO can log in",                 "SSO, MFA, authentication"),
  ("Governance/IGA (SailPoint)",   "WHAT access identities SHOULD have","reviews, certification, provisioning"),
  ("CIEM (Sysdig / Wiz)",          "cloud PERMISSIONS visibility",    "detect over-privilege (Entitle prevents it)"),
]
print("BeyondTrust/PAM in the identity-security landscape:\n")
print(f"   {'pillar':32}{'answers':38}mechanisms")
for pillar, answers, mech in LANDSCAPE:
    print(f"   {pillar:32}{answers:38}{mech}")
print("\nIdentity is the modern PERIMETER; PRIVILEGED identity is its most sensitive core,")
print("and PAM is the specialty that secures it. A PAM engineer who gets vaulting, least")
print("privilege, session management, and JIT defends against the credential-abuse attacks")
print("behind most breaches (Ch 2) — a high-demand profile.")
print("\nThe rounded identity-security engineer combines:")
print("  AUTHENTICATE (Ping/Okta)      — who logs in (SSO/MFA)")
print("  GOVERN       (SailPoint/IGA)  — what access is appropriate, reviewed")
print("  PRIVILEGE    (BeyondTrust/PAM)— secure the DANGEROUS access (the differentiator)")
print("  CLOUD PERMS  (Entitle + CIEM) — JIT + detect over-privilege in cloud/SaaS")
print("\nBeyondTrust is the PAM heart of it. Learn it alongside CyberArk (the peer), plus")
print("access management + governance + CIEM — that's an identity-security career, and PAM")
print("is its highest-stakes specialty: the access attackers want most, made hard to abuse.")
EOF
```

**Expected result:** PAM mapped against access management (Ping/Okta), governance (SailPoint), and CIEM (Sysdig/Wiz), showing the authenticate/govern/privilege/cloud-perms profile. The career-positioning lesson closes the volume: identity is the modern perimeter and privileged identity its most sensitive core, so PAM (BeyondTrust, alongside peer CyberArk) is the highest-stakes specialty within an identity-security career that also spans access management, governance, and CIEM.

**Negative test:** Treating PAM as separate from the rest of identity security. Vaulting and least privilege only fully protect when paired with strong authentication (Ping/Okta), governance (SailPoint), and cloud-permission control (Entitle/CIEM); PAM is one pillar of an integrated identity program.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] A BeyondTrust path sequenced by role and product, anchored on Password Safe for PAM roles.
- [ ] Currency understood — the two-year renew-by-retraining cycle as a genuine refresh of product skill.
- [ ] BeyondTrust/PAM positioned in the identity-security career alongside CyberArk, SailPoint, Ping/Okta, and CIEM.
- [ ] The volume assembled into a personal study and career plan — authenticate, govern, privilege, cloud permissions.
