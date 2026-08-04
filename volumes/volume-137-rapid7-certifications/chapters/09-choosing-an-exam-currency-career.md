# Chapter 09: Choosing an Exam, Currency, and Career

## Learning Objectives

- Choose the Rapid7 exam matching your role and your organization's deployment.
- Plan around the purchase-order enrollment path.
- Place Rapid7 among the encyclopedia's vulnerability-management and SIEM volumes.
- Use Academy training for ISC2/ISACA continuing-education credit.

## Choosing an exam

| If you… | Take | Chapters |
|:---|:---|:---|
| Run the vulnerability management program | **InsightVM Certified Administrator** | 02–05 |
| Work in the SOC on detection and response | **InsightIDR Certified Specialist** | 02, 06, 07 |
| Own application security testing | **InsightAppSec Certified Specialist** | 08 |
| Build security automation | **InsightConnect Certified Specialist** | 07, 08 |

There is **no prescribed ladder** — the four exams are peers covering different products, so the choice follows what your organization actually runs and what you actually do. If your employer runs InsightVM and InsightIDR, those two are the pair worth holding.

A practical route worth knowing: **virtual instructor-led courses include one exam attempt**. If your organization is buying training anyway, the certification comes with it, which sidesteps the separate purchase entirely.

## Plan around the enrollment path

Repeating from Chapter 01 because it changes timelines:

- Exams cost **$215** and are purchased **by purchase order**, then enrolled with a **promo code** from your registration email. This is not a card checkout.
- If you are an individual without a procurement relationship, the **VILT course route** (which includes an attempt) is usually more practical.
- Question count, duration, passing score, validity, and retake policy are **not published** on the Academy pages. Check your registration email and the Academy when you enroll, and treat any third-party figure as unverified.

## Continuing education credit

Rapid7 courses carry **16–24 CPE credits**. If you hold an [ISC2](../../volume-040-isc2-certifications/README.md) credential (CISSP, SSCP, CCSP) or an ISACA one ([Volume XLIV](../../volume-044-isaca-certifications/README.md)), those renewals require CPEs regardless — so training you would take for the job also services the obligation. Submit as you complete courses rather than reconstructing them at renewal.

## Where Rapid7 sits in the encyclopedia

Rapid7 completes the **vulnerability management trio** and contributes to the SIEM shelf:

- **Vulnerability management:** [Tenable LXXVIII](../../volume-078-tenable-certifications/README.md), [Qualys LXXIX](../../volume-079-qualys-certifications/README.md), and **Rapid7 (this volume)**. All three solve the same problem — discover, assess, prioritize, drive remediation — and the *discipline* transfers completely between them. Learn one properly and the others are a vocabulary exercise.
- **SIEM and detection:** [Splunk XLV](../../volume-045-splunk-certifications/README.md) and [Elastic LXXXVI](../../volume-086-elastic-certifications/README.md) alongside InsightIDR.
- **Endpoint:** [CrowdStrike L](../../volume-050-crowdstrike-certifications/README.md).
- **The broader program:** [Enterprise Cybersecurity X](../../volume-010-enterprise-cybersecurity/README.md).

Rapid7's distinctive contributions to this shelf are **deception technology** as a first-class detection method (Chapter 07) and the tight coupling of vulnerability management with detection and automation in one platform.

## Currency

- **The exam catalog is small and may change.** Four exams today; InsightCloudSec and Metasploit have training but **no certification**. Verify the current list on the Academy before planning.
- **Unpublished mechanics** (duration, questions, passing score, validity) are the thing to confirm at enrollment. This volume deliberately does not assert them — see [Volume CXXXIV](../../volume-134-solarwinds-certifications/README.md) for the same discipline applied to SolarWinds.
- **Verified 4 August 2026** from academy.rapid7.com and rapid7.com/services/training-certification: the four exams, the $215 fee, the purchase-order and promo-code enrollment path, the Academy's five content types, the 16–24 CPE credits, and the exam-preparation resources for InsightVM.

## Hands-On Lab

### Lab 9.1 — Build your Rapid7 certification plan

**Objective:** Choose an exam and a realistic route to sitting it.

```bash
cat > my-rapid7-plan.md <<'EOF'
Products my organization runs:  InsightVM / InsightIDR / InsightAppSec / InsightConnect
My role:                        VM program / SOC analyst / AppSec / automation
Target exam:                    ____________________________________  ($215)
Route to the exam:
   [ ] VILT course (INCLUDES one exam attempt) — simplest if training is being bought anyway
   [ ] Direct exam purchase — requires a PURCHASE ORDER, then a promo code from the
       registration email. Not a card checkout; involve procurement EARLY.
Free/low-cost prep:             Rapid7 Academy on-demand modules, product workshops (<=1 hr),
                                InsightVM Certified Administrator Exam Preparation +
                                InsightVM Exam Overview and Sample Questions
CPE credits:                    16-24 per course -> submit toward ISC2 / ISACA renewals
CONFIRM AT ENROLLMENT (not published): duration, question count, passing score,
                                validity period, retake policy
Practice:                       model coverage, prioritization, SLAs, log pipelines,
                                deception, and playbooks free in Python
EOF
cat my-rapid7-plan.md
```

**Expected result:** A plan that picks one exam, names the realistic route to sitting it, and lists explicitly the facts to confirm rather than assume. The purchase-order line is the one that changes calendars — discovering it the week you hoped to certify is a needless delay.

**Negative test:** Planning around a validity period or passing score quoted by a third-party site — Rapid7 does not publish those, so any figure you find elsewhere is unsourced.

**Cleanup:** Keep the plan.

### Lab 9.2 — Self-assess against the exam scopes

**Objective:** Find the weak area for your target exam.

```bash
python3 - <<'EOF'
domains = {
  "Insight platform architecture (ch02)":     3,
  "Discovery & assessment (ch03)":            4,
  "Analyze & prioritize (ch04)":              2,
  "Communicate & remediate (ch05)":           2,
  "Log collection & pipeline (ch06)":         1,
  "Detections, alerts, deception (ch07)":     1,
  "SOAR & AppSec (ch08)":                     2,
}
print("Self-rated confidence (0-5):\n")
for d, s in sorted(domains.items(), key=lambda kv: kv[1]):
    print(f"{d:42} [{'#'*s}{'.'*(5-s)}] {'STUDY FIRST' if s <= 2 else ('review' if s < 4 else 'ready')}")

exams = {
  "InsightVM Certified Administrator": ["ch02","ch03","ch04","ch05"],
  "InsightIDR Certified Specialist":   ["ch02","ch06","ch07"],
  "InsightAppSec Certified Specialist":["ch08"],
  "InsightConnect Certified Specialist":["ch07","ch08"],
}
print("\nChapter coverage per exam:")
for e, chs in exams.items():
    print(f"  {e:38} {', '.join(chs)}")
print("\nThis profile is VM-strong and detection-weak: InsightVM is nearly ready (only ch04/ch05")
print("need work), while InsightIDR needs ch06 AND ch07 from a low base. Sit the exam your")
print("current knowledge supports, and study toward the other rather than splitting effort.")
EOF
```

**Expected result:** The profile shows the vulnerability-management chapters strong and the detection chapters weak, so InsightVM is the near-term exam and InsightIDR the study target. That sequencing advice — certify where you are strong, then study toward the second — is more useful than treating every low score as equally urgent, because the four exams are independent rather than laddered.

**Negative test:** Studying all eight technical chapters evenly for the InsightAppSec exam — its scope is essentially one chapter, and the rest earns nothing toward that credential.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] A target exam chosen from the four, matched to products actually deployed.
- [ ] The purchase-order enrollment path planned for, with the VILT route considered.
- [ ] CPE credits recorded toward ISC2/ISACA renewals.
- [ ] Rapid7 placed with Tenable and Qualys, and alongside Splunk/Elastic for SIEM.
- [ ] Unpublished exam mechanics flagged for confirmation at enrollment.
