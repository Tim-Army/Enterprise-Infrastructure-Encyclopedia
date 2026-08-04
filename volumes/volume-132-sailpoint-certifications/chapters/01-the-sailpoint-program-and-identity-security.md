# Chapter 01: The SailPoint Program and Identity Security

![The SailPoint Professional Certification and Credentialing Program in Identity University, showing two parallel tracks: three training-gated Knowledge Credentials (Identity Security Leader, free path with up to 45 minutes for up to 30 questions and three free attempts; Identity Security Professional, up to 90 minutes for up to 51 questions; Identity Security Expert, up to 90 minutes for up to 65 questions, all online, immediate, adaptive, with badges that never expire), and four proctored role-based Professional Certifications (Certified Identity Security Administrator and Certified Identity Security Engineer on Identity Security Cloud at 400 dollars each; Certified IdentityIQ Associate at 300 dollars and Certified IdentityIQ Engineer at 400 dollars on on-premises IdentityIQ, each with 364 days to schedule and two attempts included, renewed on a two-year recertification cycle). Both tracks rest on the identity governance and administration disciplines this volume teaches: identity data and sources, access modeling, lifecycle management and provisioning, governance and compliance, platform and virtual appliances, and rules, transforms, and workflows.](../../../diagrams/volume-132-sailpoint-certifications/chapter-01-certification-program.svg)

*Figure 1-1. SailPoint's two-track program — self-serve Knowledge Credentials and proctored Professional Certifications — across Identity Security Cloud and IdentityIQ.*

## Learning Objectives

- Describe SailPoint's two-track program: Knowledge Credentials and Professional Certifications.
- Distinguish Identity Security Cloud (SaaS) from IdentityIQ (on-premises) and pick the right track.
- Place identity governance and administration (IGA) among the encyclopedia's other identity disciplines.
- Set up a free study environment for the identity-governance labs.

## What SailPoint does

SailPoint is an **identity security** vendor whose products answer a deceptively simple governance question: **who has access to what, should they, and can you prove it?** That is the discipline of **Identity Governance and Administration (IGA)** — distinct from, and complementary to, the neighboring identity disciplines:

| Discipline | Question it answers | Encyclopedia volume |
|:---|:---|:---|
| **Access management / SSO** | Can this user authenticate and get in *right now*? | [Okta LXXVI](../../volume-076-okta-certifications/README.md) |
| **Privileged access (PAM)** | How are *administrative* credentials vaulted and brokered? | [CyberArk LXXVII](../../volume-077-cyberark-certifications/README.md) |
| **Identity governance (IGA)** | *Should* this user have this access — who approved it, when was it reviewed, and is it still appropriate? | **This volume** |

IGA is the auditor's half of identity. It aggregates accounts and entitlements from every connected system into a single identity model, decides what access each person *should* hold (roles, policies), provisions and deprovisions it as people join/move/leave, and produces the **evidence** — certification campaigns, policy-violation records, audit trails — that regulators and auditors demand.

SailPoint sells this in two product lines, and the certification program is organized around them:

- **Identity Security Cloud (ISC)** — the SaaS platform; the modern, primary track.
- **IdentityIQ (IIQ)** — the on-premises product; still widely deployed, with its own certification pair.

A newer product path, **SailPoint Agentic Fabric**, extends identity security to agentic AI — a reminder that this program moves.

## The two tracks

The organizing insight of SailPoint's program is that it offers **two genuinely different kinds of credential**, aimed at different people and earned in different ways:

| | **Knowledge Credentials** | **Professional Certifications** |
|:---|:---|:---|
| Proves | You learned the material | You have real-world, role-based expertise |
| Gate | Complete the training path first | Experience recommended (6 months–1 year) |
| Delivery | Online, immediate, no scheduling | Proctored, scheduled |
| Cost | **Free** for your first attempts | **$300–$400** |
| Attempts | 2–3 free | **2 included** with enrollment |
| Expiry | Badge **never expires** | **Recertify every 2 years** |

Knowledge Credentials serve as the "final exam" for a training path; Professional Certifications are the rigorous, proctored credential for seasoned practitioners. Badges issue through Identity University and **Credly**.

### Knowledge Credentials (3)

| Credential | Focus | Exam |
|:---|:---|:---|
| **Identity Security Leader** | Product-agnostic foundation: identity-security concepts, terms, best practices, for those who lead or support an identity program | Free path; **3 free attempts**; ≤45 min, ≤30 questions |
| **Identity Security Professional** | ISC architecture, identity data management, certifications, policies, access modeling | **2 free attempts**; ≤90 min, ≤51 questions |
| **Identity Security Expert** | ISC transforms, rules, workflows, event triggers, APIs, connectivity | **2 free attempts**; ≤90 min, ≤65 questions |

All three are **adaptive**: the exam may end early once you have reached the required number of correct (or incorrect) answers, and results are automatic. They must be taken in one sitting — no pausing, no changing a submitted answer.

### Professional Certifications (4)

| Certification | Product | Experience recommended | Price |
|:---|:---|:---|:---|
| **SailPoint Certified Identity Security Administrator** | Identity Security Cloud | 6 months | $400 |
| **SailPoint Certified Identity Security Engineer** | Identity Security Cloud | 1 year | $400 |
| **SailPoint Certified IdentityIQ Associate** | IdentityIQ | 1 year | $300 |
| **SailPoint Certified IdentityIQ Engineer** | IdentityIQ | 1 year | $400 |

Enrollment mechanics are uniform: after registering you have **364 days** to schedule and sit the exam, and **two attempts are included** (status reads Passed, Not Complete, or Not Passed).

The **Identity Security Administrator** certification is the program's newest, launched alongside the **Recertification Program** in February 2026 — which extends a certification for **two years** through training, projects, events, and similar activity, rather than a re-sit. That launch made seven exams in total, serving a community of **over 12,000 SailPoint certified professionals** — a population that quadrupled in the preceding year.

## How the domains map to this volume

The exam domains across the four certifications are strikingly consistent, and they set this volume's chapter structure:

| Exam domain (SailPoint's words) | Chapter |
|:---|:---|
| Sources; identity data | [02](02-identity-data-model-and-sources.md) |
| Access Management; access modeling | [03](03-access-modeling.md) |
| Identity and Lifecycle Management; Provisioning | [04](04-lifecycle-management-and-provisioning.md) |
| Supporting Governance; policies; certifications | [05](05-governance-and-compliance.md) |
| Platform; Virtual Appliances; connectivity | [06](06-platform-virtual-appliances-connectivity.md) |
| Architecture; **Rules and Transforms**; workflows, event triggers, APIs | [07](07-rules-transforms-workflows-apis.md) |
| IdentityIQ install/build/deploy; Lifecycle Manager; custom development; application onboarding; debugging | [08](08-identityiq-on-premises.md) |

Note the split that separates the two ISC certifications: the **Administrator** exam covers Platform, Virtual Appliances, Identity and Lifecycle Management, Provisioning, Access Management, Supporting Governance, and Sources; the **Engineer** exam adds **Architecture** and **Rules and Transforms** — the build-and-extend material in Chapter 07. That is the practical difference between operating the platform and engineering on it.

## Free study environment

SailPoint's products are commercial and licensed, so this volume's labs model the **IGA disciplines** — identity correlation, role mining, joiner-mover-leaver state machines, separation-of-duties evaluation, certification campaigns, transforms — in free Python. The concepts transfer directly to ISC and IdentityIQ; no SailPoint software is required.

## Hands-On Lab

### Lab 1.1 — Set up the study environment

**Objective:** Confirm the free toolchain for every lab in this volume.

```bash
python3 --version
mkdir -p ~/sailpoint-study && cd ~/sailpoint-study
python3 - <<'EOF'
print("IGA study environment ready.")
print("Labs model: identity correlation, access modeling, JML provisioning,")
print("certification campaigns, SoD policy, transforms/workflows — no SailPoint license needed.")
EOF
```

**Expected result:** Python 3 reports a version and the message prints. Everything in this volume runs on the standard library — the IGA logic, not the vendor UI, is what the exams test and what transfers between ISC and IdentityIQ.

**Negative test:** Assuming you must have a licensed tenant to study IGA — the governance model (identities, entitlements, roles, policies, campaigns) is vendor-independent; you can build and reason about all of it locally.

**Cleanup:** `rm -rf ~/sailpoint-study` when finished with the volume.

### Lab 1.2 — Map the program to a plan

**Objective:** Choose your track from the two-track structure.

```bash
python3 - <<'EOF'
def recommend(role, product, experience_months, budget):
    if budget == 0:
        return "Knowledge Credentials: Identity Security Leader (free path, 3 free attempts) -> Professional -> Expert"
    if product == "IdentityIQ":
        return "IdentityIQ Associate ($300) -> IdentityIQ Engineer ($400)"
    if experience_months < 12:
        return "Certified Identity Security Administrator ($400, 6 months experience recommended)"
    return "Certified Identity Security Engineer ($400, 1 year experience; adds Architecture + Rules/Transforms)"

for case in [("leader","ISC",3,0), ("admin","ISC",8,400), ("engineer","ISC",18,400), ("engineer","IdentityIQ",14,400)]:
    print(f"{case}: {recommend(*case)}")
EOF
```

**Expected result:** A zero budget routes to the free Knowledge Credential ladder; IdentityIQ shops route to the on-premises pair; ISC candidates split at roughly a year of experience between Administrator and Engineer. The decisive variables are **product line** (ISC vs IdentityIQ) and **role** (operate vs engineer) — exactly the two axes SailPoint's program is built on.

**Negative test:** Booking the Engineer exam with no exposure to rules and transforms — that material (Chapter 07) is what distinguishes it from the Administrator exam; the recommended year of hands-on experience is a real signal, not a formality.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] The two tracks distinguished: Knowledge Credentials (free, training-gated, never expire) vs Professional Certifications (proctored, paid, 2-year recertification).
- [ ] All seven exams named, with their products, experience expectations, and prices.
- [ ] ISC vs IdentityIQ understood as the program's product split.
- [ ] IGA placed against access management (Okta) and PAM (CyberArk).
- [ ] Free Python study environment ready.
