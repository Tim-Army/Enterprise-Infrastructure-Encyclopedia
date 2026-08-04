# Chapter 09: Choosing a Level, Recertification, and Career

## Learning Objectives

- Choose and sequence Everpure certifications for your role.
- Exploit both recertification paths deliberately.
- Place Everpure among the encyclopedia's storage and data-protection volumes.
- Keep current with a vendor that has just rebranded.

## Choosing a path

| If you… | Take | Chapters |
|:---|:---|:---|
| Are new to the platform | **Associate: Data Storage** ($200) | 01–04 |
| Operate block storage daily | **Professional: FlashArray Storage** ($300) | 02, 03, 05, 06 |
| Operate file/object storage | **Professional: FlashBlade Storage** ($300) | 04, 05 |
| Run Kubernetes storage | **Professional: Portworx Enterprise** ($300) | 08 |
| Own data protection and ransomware readiness | **Professional: Cyber Resilience** ($300) | 06, 07 |
| Deploy arrays | **Specialist: FlashArray/FlashBlade Implementation** ($300) | 02–04 |
| Troubleshoot arrays | **Specialist: FlashArray/FlashBlade Support** ($300) | 03, 04, 06 |
| Work in cloud or migrations | **Specialist: Cloud** or **Migration** ($300) | 04, 06 |
| Design whole solutions | **Expert: Platform Architect** ($400) | all |

**Start with the Associate**, for a reason that is more than convention: it costs $200, covers the foundations the others assume — and, critically, **renews itself automatically** once you earn any higher certification. Sit it first and it maintains itself for as long as you keep progressing.

The **Implementation versus Support** split is worth choosing deliberately rather than by availability. Implementation is about deploying correctly; Support is about diagnosing something already deployed and misbehaving. They are different skills, and the certification that matches your actual work is the one worth holding.

## Recertification, used well

Certifications are valid for **three years** and are renewed by retaking the updated exam. Two alternatives change the calculus:

1. **The Associate (DSA) renews automatically** on earning any Professional, Specialist, or Expert certification.
2. **Continuing Everpure Education (CEE) credits** apply to **select FlashArray exams** — check the individual exam page rather than assuming, since this does not apply to every exam.

A practical sequence for someone staying in the ecosystem: Associate → a Professional matching your daily work → a Specialist as your role narrows or an Expert as it broadens. Each step up renews the Associate and refreshes your knowledge on the current platform, which is the point of a three-year cycle.

Record your expiry when you pass. Three years is long enough to forget entirely.

## Preparing

The FAQ states that **training is not required** and that **"each exam is designed to test your on-the-job experience."** Take that literally: these exams reward having operated the platform. Official resources supplement that experience rather than replacing it —

- **Study Guides** and **Certification Prep Training**
- the **Everpure PEAK Customer Course Catalog** (on-demand, instructor-led, and prep training)
- the **Certification Experience Guide** (preparing, scheduling, claiming badges, maintaining certification)
- the **Everpure Knowledge Portal** and the community

Remember the exams are **closed book and proctored with a webcam** — no external materials.

## Where Everpure sits in the encyclopedia

- **Everpure (this volume)** — all-flash primary storage: block, file/object, and cloud-native, with the Evergreen non-disruptive model.
- [**NetApp LXXXIV**](../../volume-084-netapp-certifications/README.md) — the other major storage-led data-management program; the closest peer.
- [**Dell Technologies XXXII**](../../volume-032-dell-technologies-certifications/README.md) — storage among a broader infrastructure portfolio.
- [**Enterprise Storage and Data Protection VI**](../../volume-006-enterprise-storage-data-protection/README.md) — the vendor-neutral foundations.
- Data protection neighbors: [**Rubrik CXXX**](../../volume-130-rubrik-certifications/README.md), [**Commvault CXXXIII**](../../volume-133-commvault-certifications/README.md), [**Veeam LXXXV**](../../volume-085-veeam-certifications/README.md). Note the convergence — Everpure's Cyber Resilience certification covers immutability and clean recovery, which those vendors also claim. Primary storage and backup are meeting in the middle on ransomware.
- [**CNCF and Kubernetes XLI**](../../volume-041-cncf-kubernetes-certifications/README.md) — context for Portworx.

## Currency

- **The company rebranded from Pure Storage to Everpure, Inc.** Certification and product names carry both histories: certifications are "Everpure", products remain FlashArray/FlashBlade/Portworx/Evergreen, and the conference is still **Pure Accelerate**. The academy is branded Everpure but still hosted at **academy.purestorage.com** — an old-looking URL that is entirely current.
- **Exam content follows the platform**, which ships continuously; the three-year validity exists precisely because the product moves.
- **Verified 4 August 2026** from academy.purestorage.com and everpuredata.com: the twelve certifications across four levels, the $200/$300/$400 pricing, proctored closed-book multiple-choice delivery, three-year validity, DSA auto-renewal, and CEE credits for select FlashArray exams.

## Hands-On Lab

### Lab 9.1 — Build your Everpure certification plan

**Objective:** Sequence certifications so the Associate maintains itself.

```bash
cat > my-everpure-plan.md <<'EOF'
Products I work with:  FlashArray / FlashBlade / Portworx / Evergreen//One
My role:               operate / implement / support / architect
STEP 1:  Associate — Data Storage (DSA)          $200
         ...sit this FIRST: it auto-renews when you earn any higher certification
STEP 2:  Professional matching daily work        $300
         FlashArray Storage | FlashBlade Storage | Portworx Enterprise | Cyber Resilience
STEP 3:  Specialist (narrow) or Expert (broaden) $300 / $400
         Implementation = deploying   |   Support = diagnosing   (choose by your actual job)
Exam day:   multiple choice, ONLINE PROCTORED with webcam, CLOSED BOOK
            training not required — exams test on-the-job experience
Validity:   3 years.  EXPIRY DATE: ______________
Renewal:    retake the updated exam  OR
            DSA: automatic when a higher cert is earned  OR
            CEE credits — SELECT FlashArray exams only (check the exam page)
Prepare:    Study Guides · Certification Prep Training · PEAK Course Catalog ·
            Certification Experience Guide · Knowledge Portal
Practice:   model upgrades, mappings, reduction ratios, RPO, immutability, K8s PVs in Python
EOF
cat my-everpure-plan.md
```

**Expected result:** A plan that sits the Associate first to exploit auto-renewal, then progresses by role, and records the expiry date at pass time. The Implementation-versus-Support note is deliberate: choosing by what you actually do produces a more credible credential than choosing by whichever exam is scheduled soonest.

**Negative test:** Skipping the Associate to go straight to a Professional — you forgo a $200 credential that would then have maintained itself for free, and you sit the higher exam without the foundation it assumes.

**Cleanup:** Keep the plan.

### Lab 9.2 — Self-assess against the exam scopes

**Objective:** Find the weak domain for your target certification.

```bash
python3 - <<'EOF'
domains = {
  "Flash architecture & Evergreen (ch02)":  3,
  "FlashArray fundamentals (ch03)":         4,
  "FlashBlade & unstructured (ch04)":       2,
  "Data reduction & efficiency (ch05)":     2,
  "Protection & replication (ch06)":        3,
  "Cyber resilience (ch07)":                1,
  "Portworx & cloud-native (ch08)":         1,
}
print("Self-rated confidence (0-5):\n")
for d, s in sorted(domains.items(), key=lambda kv: kv[1]):
    print(f"{d:42} [{'#'*s}{'.'*(5-s)}] {'STUDY FIRST' if s <= 2 else ('review' if s < 4 else 'ready')}")

exams = {
  "Associate: Data Storage":        ["ch02","ch03","ch04"],
  "Prof: FlashArray Storage":       ["ch02","ch03","ch05","ch06"],
  "Prof: FlashBlade Storage":       ["ch04","ch05"],
  "Prof: Portworx Enterprise":      ["ch08"],
  "Prof: Cyber Resilience":         ["ch06","ch07"],
  "Expert: Platform Architect":     ["ch02","ch03","ch04","ch05","ch06","ch07","ch08"],
}
print("\nChapter coverage per certification:")
for e, chs in exams.items():
    print(f"  {e:30} {', '.join(chs)}")
print("\nThis profile is FlashArray-strong and weak on cyber resilience and Portworx.")
print("FlashArray Storage is the near-term exam (only ch05 needs work); Cyber Resilience and")
print("Portworx each need two low-scoring chapters. Certify where you are strong, study toward the rest.")
EOF
```

**Expected result:** The profile shows FlashArray Storage within reach while Cyber Resilience and Portworx each require building two weak areas. The sequencing advice — certify where you are strong, then study toward the next — suits a program of independent peer certifications rather than a strict ladder.

**Negative test:** Studying all seven technical chapters evenly for the Portworx exam — its scope is essentially one chapter, and the rest earns nothing toward that credential.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] A role-matched certification chosen, with the Associate sat first for auto-renewal.
- [ ] Implementation and Support distinguished as different jobs.
- [ ] Both recertification paths understood, including CEE's limitation to select FlashArray exams.
- [ ] Everpure placed against NetApp, Dell, and the data-protection volumes.
- [ ] The rebrand's effect on names and URLs recorded for future searching.
