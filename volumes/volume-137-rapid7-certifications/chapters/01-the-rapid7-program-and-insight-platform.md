# Chapter 01: The Rapid7 Program and the Insight Platform

![The Rapid7 certification program in the Rapid7 Academy: four certification exams at 215 US dollars each — InsightVM (Rapid7 Vulnerability Management) Certified Administrator, InsightIDR (Rapid7 SIEM) Certified Specialist, InsightAppSec (Rapid7 Application Security) Certified Specialist, and InsightConnect (Rapid7 Automation) Certified Specialist. Exams are purchased by purchase order and enrolled with a promo code from the registration email, and virtual instructor-led courses include one exam attempt. The Academy offers five content types: on-demand training, product and technology demonstrations, virtual instructor-led courses with lab environments, certification exams, and short product workshops, with courses carrying 16 to 24 CPE credits. InsightCloudSec and Metasploit have training courses but no certification exam.](../../../diagrams/volume-137-rapid7-certifications/chapter-01-certification-program.svg)

*Figure 1-1. Rapid7's four certification exams, the Academy content types beneath them, and the products that have training but no exam.*

## Learning Objectives

- Describe the Rapid7 certification program and its four exams.
- Explain the Insight platform's components and how data reaches it.
- Distinguish products that carry certifications from those that carry only training.
- Set up a free study environment for the defensive labs in this volume.

## What Rapid7 does

Rapid7 sells a security operations portfolio built around the **Insight platform** — a cloud back end fed by agents and collectors deployed in your environment. The products that matter for certification:

| Product | Discipline |
|:---|:---|
| **InsightVM** | Vulnerability management — find, prioritize, and drive remediation of weaknesses |
| **InsightIDR** | SIEM and detection/response — collect logs, detect attacks, investigate |
| **InsightAppSec** | Application security — dynamic scanning of web applications |
| **InsightConnect** | Security orchestration and automation (SOAR) — playbooks that act |

This volume is **defensive throughout**. Rapid7 also stewards Metasploit, and offensive tooling is out of scope here; where attacker behavior appears, it appears so you can detect and remediate it.

## The certification program

Certification runs through the **Rapid7 Academy**, and the exam catalog is small and precise:

| Exam | Credential name |
|:---|:---|
| **InsightVM (Rapid7 Vulnerability Management)** | Certified **Administrator** |
| **InsightIDR (Rapid7 SIEM)** | Certified **Specialist** |
| **InsightAppSec (Rapid7 Application Security)** | Certified **Specialist** |
| **InsightConnect (Rapid7 Automation)** | Certified **Specialist** |

Two things to notice. First, the **naming is not uniform** — InsightVM produces a *Certified Administrator* while the other three produce *Certified Specialists*. Second, Rapid7 puts a **category gloss** in each exam name ("Rapid7 SIEM", "Rapid7 Automation"), which is genuinely helpful: it tells you what the product *is* if you know the discipline but not the brand name.

### Enrollment has a wrinkle worth knowing

Exams cost **$215** each, and the purchasing path is unusual:

> You purchase certification exams **via a purchase order**. When you enroll for an exam, you are prompted for the **promo code provided in your registration email**.

This is not a card-and-go checkout. If you are an individual rather than a customer organization with a procurement relationship, plan for that friction before setting an exam date. Virtual instructor-led courses **include one exam attempt**, which for many candidates is the practical route to the credential.

### Products with training but no exam

**InsightCloudSec** (cloud security) and **Metasploit** have Academy courses and workshops but **no certification exam** in the catalog. That distinction matters when planning: you can be trained on them, and there is no credential to earn. Anyone advertising a "Rapid7 InsightCloudSec certification" is describing something the vendor does not currently offer.

### What is not published

Rapid7 does not publish question counts, exam duration, passing scores, validity periods, or retake policy on its Academy pages. This volume therefore does not assert them. Your **registration email** and the Academy are the authoritative sources — check them when you enroll, and treat any third-party figure with suspicion.

There *are* official preparation resources: an **InsightVM Certified Administrator Exam Preparation** listing and an **InsightVM Exam Overview and Sample Questions** page.

## The Rapid7 Academy

The Academy organizes learning into five content types:

| Type | Shape |
|:---|:---|
| **On-Demand Training** | Self-paced e-learning; always available |
| **Product and Technology Demonstrations** | Video overviews of product value |
| **Virtual Instructor-Led Training** | 1–2 day courses over Zoom, restricted class size, **virtual lab environment**, and **one exam attempt included** |
| **Certification Exams** | The four exams above |
| **Product Workshops** | Live, one hour or less, configuration-focused |

A public **Training Calendar** lists scheduled sessions, and courses carry **16–24 CPE credits** — which feed the continuing-education requirements of [ISC2](../../volume-040-isc2-certifications/README.md) credentials such as the CISSP. As with Commvault's ISC2 arrangement, training you would take anyway can also service a renewal obligation.

## Free study environment

Rapid7's products are commercial, so this volume's labs model the **disciplines** — scan coverage, credentialed-scan lift, risk prioritization against raw CVSS, remediation SLA aging, log parsing and query, deception trip-wires, alert fidelity, and playbook branching — in free Python. Those concepts are what the exams assess and what transfers to any comparable platform.

## Hands-On Lab

### Lab 1.1 — Set up the study environment

**Objective:** Confirm the free toolchain.

```bash
python3 --version
mkdir -p ~/rapid7-study && cd ~/rapid7-study
python3 - <<'EOF'
print("Security operations study environment ready.")
print("Labs model: scan coverage, credentialed-scan lift, risk prioritization,")
print("SLA aging, log pipelines, deception, alert fidelity, SOAR playbooks.")
print("Defensive throughout — no Rapid7 license required.")
EOF
```

**Expected result:** Python reports a version and the message prints. Everything runs on the standard library.

**Negative test:** Assuming you need a licensed Insight tenant to study — prioritization logic, SLA arithmetic, and detection tuning are vendor-independent reasoning, and that reasoning is what the exams test.

**Rollback:** `rm -rf ~/rapid7-study` when finished.

### Lab 1.2 — Choose an exam and plan around the enrollment path

**Objective:** Match exam to role, and account for the purchase-order route.

```bash
python3 - <<'EOF'
EXAMS = {
  "vulnerability management": ("InsightVM (Rapid7 Vulnerability Management) Certified Administrator", 215),
  "SIEM / detection & response": ("InsightIDR (Rapid7 SIEM) Certified Specialist", 215),
  "application security":     ("InsightAppSec (Rapid7 Application Security) Certified Specialist", 215),
  "security automation (SOAR)":("InsightConnect (Rapid7 Automation) Certified Specialist", 215),
}
for role, (exam, fee) in EXAMS.items():
    print(f"{role:28} -> ${fee}  {exam}")

NO_EXAM = ["InsightCloudSec (cloud security)", "Metasploit"]
print("\nTraining exists, NO certification exam:")
for p in NO_EXAM:
    print(f"   - {p}")

print("\n--- enrollment path (plan for this) ---")
def route(has_po_process, taking_vilt):
    if taking_vilt:
        return "VILT course INCLUDES one exam attempt — usually the simplest route"
    if has_po_process:
        return "Purchase via PURCHASE ORDER, then enroll with the promo code from your registration email"
    return ("BLOCKED for now — exams are bought by purchase order, not card checkout. "
            "Work through your organization's procurement, or take a VILT course instead")
for po, vilt in [(True, False), (False, False), (False, True)]:
    print(f"  purchase-order process={str(po):5} taking VILT={str(vilt):5} -> {route(po, vilt)}")
EOF
```

**Expected result:** Each discipline maps to one exam at $215, the two products without exams are named explicitly, and the enrollment check shows that an individual without a procurement process is effectively steered toward the instructor-led course. That is a real planning constraint, and it is better discovered now than on the day you decide to certify.

**Negative test:** Budgeting only the $215 and assuming you can book tonight — the purchase-order step involves your organization and takes as long as it takes.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] The four exams named, with the Administrator/Specialist naming difference noted.
- [ ] The $215 fee and purchase-order/promo-code enrollment path understood.
- [ ] InsightCloudSec and Metasploit identified as training-only, with no certification exam.
- [ ] Academy content types and the 16–24 CPE credit benefit recorded.
- [ ] Unpublished exam details (duration, questions, passing score, validity) flagged for checking at enrollment.
