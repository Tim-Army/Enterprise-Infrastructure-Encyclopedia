# Chapter 01: The BeyondTrust University Certification Program

![The BeyondTrust University certification program and the PAM platform beneath it. BeyondTrust University issues one Certified Administrator credential per product, delivered as Credly verified digital badges. Each certification is granted on completion of the required Instructor-Led Training course plus a passing score of seventy-five percent or higher on a forty-question exam, delivered online through the BTU portal, open note but completed independently, with two attempts allowed and immediate results. Certifications are valid for two years and renew by purchasing new training and passing again, and each course grants up to sixteen hours of Continuing Professional Education credit. Eight Certified Administrator programs cover the BeyondTrust product line: AD Bridge, Endpoint Privilege Management for Linux, Mac, and Windows, Password Safe, Privileged Remote Access, Remote Support, and Entitle. The platform beneath is Privileged Access Management, the discipline of securing, controlling, and monitoring privileged access, which is the single most common path in a breach.](../../../diagrams/volume-156-beyondtrust-certifications/chapter-01-program.svg)

*Figure 1-1. The Certified Administrator credentials, their uniform exam mechanics, and the PAM platform they validate.*

## Learning Objectives

- Describe the BeyondTrust University program — one Certified Administrator credential per product.
- State the uniform exam mechanics precisely (ILT, 40 questions, 75%, 2 attempts, 2-year validity, CPE).
- Place the eight products the certifications cover.
- Recognize BeyondTrust's position as a Privileged Access Management (PAM) leader.

> **Defensive framing.** This volume is about *defending* privileged access — vaulting credentials, enforcing least privilege, brokering remote sessions, and monitoring what administrators do. PAM is a defensive control discipline: it shrinks the attack surface that privileged accounts represent. Nothing here is about attacking systems.

## What BeyondTrust is

BeyondTrust is a leader in **Privileged Access Management (PAM)** — the discipline of securing, controlling, and monitoring **privileged access** (administrator, root, and service accounts) across an enterprise. Privileged accounts are the **crown jewels**: a compromised admin credential lets an attacker do anything that account can, so PAM is one of the highest-leverage defensive controls. BeyondTrust's product line spans credential vaulting, endpoint least privilege, remote access, and cloud entitlements, and its **BeyondTrust University (BTU)** program certifies administrators on each.

The other PAM leader this shelf covers is [CyberArk (LXXVII)](../../volume-077-cyberark-certifications/README.md); **BeyondTrust versus CyberArk** is the defining PAM comparison, and understanding one sharpens the other.

## The program

BTU's credential is the **BeyondTrust Certified Administrator**, issued as **Credly** verified digital badges — **one per product.** It is a *badges-and-training* model built on instructor-led training, stated plainly:

> **Certified Administrator, per product.** Each certification is granted on completion of the **required Instructor-Led Training (ILT)** course *and* a passing score on the exam. There is no multi-level ladder — "Administrator" is the tier, earned once per product an administrator operates.

## Exam mechanics

The mechanics are **uniform across all eight products** — worth knowing exactly:

| Element | Value |
|:---|:---|
| **Prerequisite** | Required **Instructor-Led Training (ILT)** course |
| **Passing score** | **75% or higher** |
| **Questions** | **40 per attempt**, randomly drawn from rotating pools (unique each time) |
| **Delivery** | Online through the **BTU portal**; results immediate + email |
| **Format** | **Open note / open book**, but completed independently |
| **Attempts** | **Two**; if both fail, purchase new training for more |
| **Validity** | **2 years**; renew by purchasing new training + passing again |
| **CPE** | **Up to 16 hours** of Continuing Professional Education credit per course |

The lab models this rule set. The open-book-but-independent, ILT-gated, two-year design tells you the credential validates **operational competence on a specific product**, refreshed as the product evolves — not memorized trivia.

## The eight products

Each Certified Administrator credential covers one product:

| Product | Secures |
|:---|:---|
| **Password Safe** | Credential vaulting, rotation, privileged session management ([Chapter 3](03-password-safe.md)) |
| **Endpoint Privilege Management** (Windows/Mac/Linux) | Least privilege on endpoints ([Chapter 4](04-endpoint-privilege-management.md)) |
| **Privileged Remote Access** | VPN-less brokered privileged access ([Chapter 5](05-privileged-remote-access.md)) |
| **Remote Support** | Secure remote support sessions ([Chapter 6](06-remote-support.md)) |
| **AD Bridge** | Extending Active Directory to Linux/Unix/Mac ([Chapter 7](07-ad-bridge.md)) |
| **Entitle** | Cloud/SaaS just-in-time access ([Chapter 8](08-entitle.md)) |

The next chapter frames the **PAM discipline** these products implement; the middle chapters take each product in turn; Chapter 9 sequences a path.

## Hands-On Lab

Python models the program. **Cost:** none.

### Lab 1.1 — Map the Certified Administrator program

**Objective:** Represent the per-product credential model and the shared mechanics.

```bash
python3 - <<'EOF'
CERTS = [
  "AD Bridge", "Endpoint Privilege Management - Linux",
  "Endpoint Privilege Management - Mac", "Endpoint Privilege Management - Windows",
  "Password Safe", "Privileged Remote Access", "Remote Support", "Entitle",
]
MECHANICS = {
  "prerequisite": "required Instructor-Led Training (ILT) course",
  "pass": "75% or higher",
  "questions": "40 per attempt (rotating pools)",
  "delivery": "online via BTU portal, immediate results",
  "format": "open note, completed independently",
  "attempts": "2 (then buy new training)",
  "validity": "2 years (renew = new training + pass again)",
  "cpe": "up to 16 CPE hours per course",
  "badges": "Credly verified digital badges",
}
print("BeyondTrust University — Certified Administrator (one per product):\n")
for i, c in enumerate(CERTS, 1):
    print(f"   {i}. BeyondTrust Certified Administrator — {c}")
print(f"\n   {len(CERTS)} products, {len(CERTS)} certifications\n")
print("Uniform exam mechanics (same across ALL products):")
for k, v in MECHANICS.items():
    print(f"   {k:12}: {v}")
print("\nThe model: ONE 'Certified Administrator' credential PER PRODUCT (no multi-level")
print("ladder), each gated on INSTRUCTOR-LED TRAINING + a 40-question / 75% exam, issued")
print("as Credly badges, valid 2 YEARS. Open-book-but-independent + ILT-gated + short")
print("validity = it validates OPERATIONAL competence on a specific product as it evolves,")
print("not memorized trivia. You certify on the products you actually operate.")
EOF
```

**Expected result:** The eight per-product Certified Administrator credentials and the uniform mechanics (ILT prerequisite, 40 questions, 75%, two attempts, two-year validity, up to 16 CPE, Credly badges). The program lesson is that BeyondTrust certifies operational competence one product at a time — instructor-led-training-gated, open-book-but-independent, and refreshed every two years — so you certify on the products you run, not on abstract theory.

**Negative test:** Expecting a single multi-level "BeyondTrust Expert" ladder like some vendors. BeyondTrust's model is per-product Certified Administrator credentials; the breadth comes from certifying on each product you operate, not from climbing tiers.

**Cleanup:** None.

### Lab 1.2 — The exam rule set as a decision

**Objective:** Reason about the two-attempt, two-year, ILT-gated design.

```bash
python3 - <<'EOF'
def outcome(passed_attempt):   # None if failed both
    if passed_attempt is None:
        return "FAILED both attempts -> must purchase NEW training to retry"
    return f"PASSED on attempt {passed_attempt} -> certified (valid 2 years)"

for scenario in [1, 2, None]:
    print(f"  {outcome(scenario)}")
print()
# renewal timeline
print("Renewal: certification valid 2 years from pass date.")
print("  year 0: pass exam -> certified")
print("  year 2: EXPIRES -> renew = purchase new training + pass the current exam again")
print("  (renewing re-teaches the CURRENT product version — not a fee-only renewal)\n")
print("Why this shape? ILT prerequisite + 2-attempt limit + paid-retraining renewal all")
print("tie the credential to CURRENT, TAUGHT product skill. PAM products change (new")
print("connectors, new session controls, cloud features); a 2-year cycle that re-runs")
print("training keeps a 'Certified Administrator' genuinely current on what they operate.")
print("The open-book format matches the job: admins USE docs; the exam tests whether you")
print("can APPLY them under the product's real mechanics, not recall them cold.")
EOF
```

**Expected result:** The two-attempt outcome path (pass on attempt 1 or 2, or buy new training) and the two-year renew-by-retraining timeline. The lesson is that the ILT prerequisite, attempt limit, and paid-retraining renewal deliberately tie the credential to current, taught product skill, and the open-book format mirrors the job (administrators apply documentation rather than memorizing it).

**Negative test:** Treating the 2-year expiry as a fee-only renewal. BeyondTrust requires purchasing new training and passing the current exam again — the renewal re-teaches the current product version, keeping the credential genuinely current.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] The program understood — BeyondTrust Certified Administrator, one Credly-badged credential per product.
- [ ] The uniform mechanics memorized — ILT prerequisite, 40 questions, 75%, two attempts, two-year validity, up to 16 CPE.
- [ ] The eight products placed against the chapters that cover them.
- [ ] BeyondTrust recognized as a PAM leader, the peer of CyberArk (LXXVII).
