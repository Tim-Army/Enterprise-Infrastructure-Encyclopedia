# Chapter 09: Choosing a Path, Recertification, Currency, and Career

## Learning Objectives

- Choose and sequence SailPoint credentials and certifications for your role.
- Use the Recertification Program to keep certifications active.
- Place SailPoint among the encyclopedia's other identity and security programs.
- Keep current with a fast-moving program.

## Choosing a path

The two decisive questions are **which product** your organization runs and **which role** you hold:

| If you… | Start with | Then |
|:---|:---|:---|
| Lead or sponsor an identity program | **Identity Security Leader** credential (free path) | — |
| Are new to Identity Security Cloud | **Identity Security Professional** credential | **Certified Identity Security Administrator** ($400) |
| Operate ISC daily (6+ months) | **Certified Identity Security Administrator** | **Certified Identity Security Engineer** |
| Build and extend ISC (1+ year) | **Identity Security Expert** credential | **Certified Identity Security Engineer** ($400) |
| Work in an IdentityIQ shop | **Certified IdentityIQ Associate** ($300) | **Certified IdentityIQ Engineer** ($400) |

A cost-effective ladder for most people: **free Knowledge Credentials first** (they cost nothing but the training time, never expire, and cover the same concepts), then the proctored certification once you have the recommended hands-on experience. The credentials are genuinely useful preparation for the certifications — the Expert credential's syllabus (transforms, rules, workflows, event triggers, APIs) is precisely the Engineer exam's differentiating material.

Budget note: each Professional Certification enrollment includes **two attempts** and gives you **364 days** to schedule, so buying early and studying deliberately is reasonable.

## Recertification

SailPoint launched its **Recertification Program in February 2026**. Certifications extend for **two years** through participation — training courses, projects, events, and similar professional activity — rather than by re-sitting the exam. Knowledge Credential badges, by contrast, **never expire**.

This is the currency discipline for this vendor: track your certification's expiry, and accumulate qualifying activity through the year rather than scrambling at renewal.

## Where SailPoint sits in the encyclopedia

Identity is three distinct disciplines, and this volume completes the set:

- **Access management / SSO** — [Okta LXXVI](../../volume-076-okta-certifications/README.md): authentication, SSO, MFA, the front door.
- **Privileged access management** — [CyberArk LXXVII](../../volume-077-cyberark-certifications/README.md): vaulting and brokering administrative credentials.
- **Identity governance and administration** — **this volume**: who *should* have access, proven with evidence.

They interlock in practice. SailPoint governs *what access is appropriate*; Okta enforces *authentication at the moment of use*; CyberArk protects *the most dangerous credentials*. An organization needs all three, and the exam-relevant framing is that IGA is the control that produces audit evidence.

Wider context: [ISC2 XL](../../volume-040-isc2-certifications/README.md) (CISSP's identity-and-access-management domain is this material at concept level), [Microsoft LXXXI–LXXXIII equivalents](../../volume-040-isc2-certifications/README.md) for Entra ID, and [Enterprise Cybersecurity X](../../volume-010-enterprise-cybersecurity/README.md) for the broader program.

## Currency

- **The program moves.** The Identity Security Administrator certification and the Recertification Program both arrived in February 2026, taking the program to **seven exams**; the certified population **quadrupled** in the preceding year, passing **12,000**. Verify the current catalog on Identity University before planning.
- **The products move faster.** Identity Security Cloud ships continuously, and **SailPoint Agentic Fabric** — identity security for agentic AI — is a new product path whose governance questions (what should an autonomous agent be allowed to access, and who certifies that?) are the frontier of this field.
- **Prices and mechanics** ($300–$400, 364 days, two attempts) were verified on Identity University on **4 August 2026**; confirm before purchasing.

## Hands-On Lab

### Lab 9.1 — Build your SailPoint certification plan

**Objective:** Commit to a role- and product-aligned path.

```bash
cat > my-sailpoint-plan.md <<'EOF'
Product in my organization:  Identity Security Cloud  /  IdentityIQ  /  both
My role:                     leader / administrator / engineer
Free first:                  Identity Security Leader  ->  Professional  ->  Expert   (badges never expire)
Then certify:                Administrator ($400, 6mo exp)  or  Engineer ($400, 1yr exp)
IdentityIQ track:            Associate ($300)  ->  Engineer ($400)
Enrollment:                  364 days to schedule, 2 attempts included
Recertification:             every 2 years via training/projects/events (program launched Feb 2026)
Practice:                    model IGA free in Python — correlation, roles, JML, SoD, campaigns
EOF
cat my-sailpoint-plan.md
```

**Expected result:** A plan that sequences free credentials before paid certifications and records the recertification obligation up front. Writing the two-year renewal into the plan at the start is the point — certifications lapse because nobody calendared the renewal, not because the work was hard.

**Negative test:** Buying the Engineer exam first with no ISC exposure — the Architecture and Rules/Transforms domains (Chapter 07) assume real build experience; the recommended year of hands-on time is a genuine signal.

**Rollback:** Keep the plan.

### Lab 9.2 — Self-assess against the exam domains

**Objective:** Find your gaps before booking.

```bash
python3 - <<'EOF'
domains = {
  "Sources & identity data (ch02)":            3,
  "Access modeling / roles (ch03)":            4,
  "Lifecycle & provisioning (ch04)":           4,
  "Governance & compliance (ch05)":            2,
  "Platform & virtual appliances (ch06)":      2,
  "Rules, transforms, workflows, APIs (ch07)": 1,
  "IdentityIQ on-premises (ch08)":             0,
}
print("Self-rated confidence (0-5):\n")
for d, score in sorted(domains.items(), key=lambda kv: kv[1]):
    bar = "#" * score + "." * (5 - score)
    verdict = "STUDY FIRST" if score <= 2 else ("review" if score < 4 else "ready")
    print(f"{d:44} [{bar}] {verdict}")
print("\nISC Administrator: ch02-06.  ISC Engineer: adds ch07 (Architecture + Rules/Transforms).")
print("IdentityIQ track: ch02-05 + ch08.")
EOF
```

**Expected result:** Weakest domains sort to the top with a STUDY FIRST verdict. The closing lines map chapters to exams, so the self-assessment converts directly into a study order: an Engineer candidate weak on Chapter 07 is weak on exactly the material that distinguishes their exam from the Administrator one.

**Negative test:** Studying the domains you enjoy — access modeling is pleasant, virtual appliances and troubleshooting are not, and the exams weight them regardless of preference.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] A product- and role-aligned path chosen across credentials and certifications.
- [ ] Free Knowledge Credentials sequenced before paid Professional Certifications.
- [ ] The two-year Recertification Program obligation recorded.
- [ ] SailPoint placed against Okta (access) and CyberArk (PAM) as the governance third.
- [ ] Currency habits installed for a fast-moving program.
