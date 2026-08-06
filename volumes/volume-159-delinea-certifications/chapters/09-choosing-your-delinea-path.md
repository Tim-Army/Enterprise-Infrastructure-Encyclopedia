# Chapter 09: Choosing Your Delinea/PAM Path

## Learning Objectives

- Sequence a Delinea certification path by tier and role.
- Understand currency for an evolving PAM/identity platform.
- Place Delinea/PAM skills in the identity-security career.
- Assemble the volume into a study and career plan.

*Cert relevance: this chapter is the meta-guide — how to navigate the Security Academy tiers [Chapter 1](01-the-delinea-program.md) laid out.*

## Sequencing your path

The Security Academy's tiers ([Chapter 1](01-the-delinea-program.md)) sequence naturally, driven by role:

| You are | Start | Then |
|:---|:---|:---|
| **New to Delinea** | **Associate** (e-learning + exam) | Engineer |
| **PAM admin / engineer** | **Associate** → **Engineer** (expert-assessed labs) | (Consultant if partner) |
| **Delinea partner / consultant** | Engineer | **Consultant** (by invitation) |

**Start at Associate** to build the technical foundation, then earn **Engineer** — the hands-on, expert-assessed credential that proves you can install, configure, and troubleshoot in production. **Consultant** is invitation-only for partners doing integrations and extensibility. Request **NFR license keys** to practice hands-on, especially for the Engineer labs. Within the tiers, focus on the **products you operate** — Secret Server first (the flagship), then Privilege Manager, Server PAM, and the rest. The lab builds a sequence.

## Currency

Delinea's platform evolves — the **unified Delinea Platform**, **ITDR/ISPM** identity-security capabilities, and DevOps/machine-identity features are all moving, and PAM itself is [converging with the wider identity stack (Ch 8)](08-the-delinea-platform-and-identity-security.md). Treat certification as a snapshot and keep current as the platform and the [threat landscape shift under the credential](../../volume-151-sentinelone-certifications/chapters/09-choosing-your-sentinelone-path.md). Because the Engineer tier is hands-on, staying current means **staying hands-on** — keep operating the platform (NFR keys help). The lab covers currency.

## The PAM / identity-security career

Delinea skills sit in the **identity-security** career — one of the highest-demand areas in the field, because identity is the modern perimeter and privileged identity its most sensitive core. A PAM engineer who understands vaulting, endpoint and server least privilege, machine secrets, service-account governance, and identity threat detection is exactly the profile enterprises need. The career pairs with the adjacent skills this shelf covers:

- **[BeyondTrust (CLVI)](../../volume-156-beyondtrust-certifications/README.md) and [CyberArk (LXXVII)](../../volume-077-cyberark-certifications/README.md)** — the other PAM leaders; knowing the **PAM trio** is a strong, portable PAM profile.
- **[SailPoint (CXXXII)](../../volume-132-sailpoint-certifications/README.md)** — identity governance (IGA); *what* access identities should have.
- **[Ping (CL)](../../volume-150-ping-identity-certifications/README.md) / [Okta (LXXVI)](../../volume-076-okta-certifications/README.md)** — access management, SSO, MFA; *who* logs in.
- **CIEM ([Sysdig CLV](../../volume-155-sysdig-certifications/README.md) / [Wiz CXLVII](../../volume-147-wiz-certifications/README.md))** — cloud entitlements, adjacent to machine identity and ISPM.

Delinea is the PAM-into-identity-security specialty. The lab positions it.

## Hands-On Lab

Python assembles a personal Delinea/PAM plan. **Cost:** none.

### Lab 9.1 — Build your Delinea path

**Objective:** Generate a tier- and product-appropriate sequence.

```bash
python3 - <<'EOF'
PATH = [
    ("Associate", "e-learning + online exam — technical foundation across use cases/config/best practice"),
    ("Engineer",  "hands-on labs assessed by a LIVE expert — install/configure/troubleshoot (break-fix)"),
    ("Consultant","(partners, BY INVITATION) — customizations, integrations, extensibility"),
]
PRODUCTS = ["Secret Server (flagship — start here)", "Privilege Manager (endpoint LP)",
            "Server PAM (server LP + AD bridging)", "DevOps Secrets Vault (machine secrets)",
            "Account Lifecycle Manager (service accounts)", "Delinea Platform + ITDR/ISPM"]
print("Delinea Security Academy path:\n")
for i, (tier, why) in enumerate(PATH, 1):
    print(f"   {i}. {tier:11} {why}")
print("\n   product focus (within the tiers), in a sensible order:")
for p in PRODUCTS:
    print(f"      - {p}")
print("\nGuidance:")
print("  - START at ASSOCIATE (foundation) -> earn ENGINEER (the hands-on, expert-graded")
print("    credential proving you can operate + troubleshoot in production).")
print("  - CONSULTANT is invitation-only (partners; integrations/extensibility).")
print("  - request NFR (Not-for-Resale) LICENSE KEYS to practice hands-on for the Engineer labs.")
print("  - focus on the PRODUCTS you operate, SECRET SERVER first (the flagship).")
print("  - CURRENCY: the platform evolves (Delinea Platform, ITDR/ISPM, machine identity) —")
print("    stay HANDS-ON, since the Engineer tier is practical.")
EOF
```

**Expected result:** The tier path (Associate → Engineer → invitation-only Consultant) with a product focus starting on Secret Server, and guidance to use NFR keys for hands-on practice. The build-your-path lesson is to start at Associate for the foundation, earn the hands-on expert-assessed Engineer credential, focus on the products you operate (Secret Server first), and stay hands-on for currency as the platform evolves.

**Negative test:** Aiming straight for Consultant. It is invitation-only for partners and assumes Engineer-level hands-on capability; build Associate → Engineer first, on the products you actually operate.

**Cleanup:** None.

### Lab 9.2 — Position Delinea in the identity-security career

**Objective:** Map Delinea/PAM skills to adjacent competencies.

```bash
python3 - <<'EOF'
LANDSCAPE = [
  ("PAM trio (Delinea / BeyondTrust / CyberArk)", "secure PRIVILEGED access", "vault, least priv, sessions, JIT"),
  ("Governance/IGA (SailPoint CXXXII)", "WHAT access is appropriate",         "reviews, certification, provisioning"),
  ("Access mgmt (Ping CL / Okta LXXVI)", "WHO logs in",                        "SSO, MFA, authentication"),
  ("ITDR / ISPM (Delinea + peers)", "DETECT identity threats + reduce risk",   "analytics, posture, response"),
  ("CIEM (Sysdig CLV / Wiz CXLVII)", "cloud PERMISSIONS",                      "entitlements, machine identity"),
]
print("Delinea in the identity-security landscape:\n")
print(f"   {'pillar':46}{'answers':38}mechanisms")
for pillar, answers, mech in LANDSCAPE:
    print(f"   {pillar:46}{answers:38}{mech}")
print("\nIdentity is the modern PERIMETER; PRIVILEGED identity is its most sensitive core.")
print("Delinea is one of the three PAM leaders (with BeyondTrust + CyberArk) — knowing the")
print("PAM TRIO is a strong, portable profile. And Delinea extends PAM into IDENTITY SECURITY")
print("(ITDR/ISPM), converging with governance (SailPoint), access mgmt (Ping/Okta), and CIEM.")
print("\nThe rounded identity-security engineer combines:")
print("  PREVENT   (PAM: vault, least privilege, MFA)   — stop privileged abuse")
print("  GOVERN    (IGA + ALM)                          — right accounts, right access")
print("  AUTHENTICATE (access mgmt)                     — who gets in")
print("  DETECT    (ITDR/ISPM + analytics)              — catch identity attacks, reduce risk")
print("Delinea covers the PREVENT core and reaches into DETECT/GOVERN — a PAM-into-identity")
print("career, learned alongside its PAM peers and the wider identity stack.")
EOF
```

**Expected result:** Delinea mapped against the PAM trio, governance (SailPoint), access management (Ping/Okta), ITDR/ISPM, and CIEM, across the prevent/govern/authenticate/detect model. The career-positioning lesson closes the volume: identity is the modern perimeter and privileged identity its core, so Delinea (one of the PAM trio) anchors the prevent layer and extends into detect/govern — a PAM-into-identity-security career learned alongside its peers and the wider identity stack.

**Negative test:** Treating PAM as a standalone silo. Privileged access is one part of identity security; Delinea skills fully pay off combined with governance, access management, and identity threat detection in an integrated identity-security program.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] A Delinea path sequenced by tier (Associate → Engineer → invitation-only Consultant) and product (Secret Server first).
- [ ] Currency understood — staying hands-on as the platform and identity-security capabilities evolve.
- [ ] Delinea positioned in the identity-security career alongside the PAM trio, governance, access management, and CIEM.
- [ ] The volume assembled into a personal study and career plan — prevent, govern, authenticate, detect.
