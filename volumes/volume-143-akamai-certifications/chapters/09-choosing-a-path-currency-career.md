# Chapter 09: Choosing a Path, Currency, and Career

## Learning Objectives

- Choose an Akamai credential path by role, across course badges and the certification tier.
- Prepare for a program that publishes badge metadata but not exam mechanics.
- Place Akamai among the encyclopedia's edge, security, and cloud volumes.
- Stay current with a program that badges continuously and restructures on acquisitions.

## Choosing

Akamai's credentials serve different purposes, so choose by what you need to *prove*:

| If you… | Pursue | Type |
|:---|:---|:---|
| Run web delivery/performance | **Web Performance Foundations → & Offload** course badges | Course completion |
| Run media delivery | **Media Delivery** course badges | Course completion |
| Operate the WAF/bot stack | **Web App & API Protection**, **Bot & Abuse Protection** course badges | Course completion |
| Architect API security | **API Security – Architect** | Certification (Advanced) |
| Operate Guardicore segmentation | **GCSA** → **GCSA Advanced** | Certification ladder |
| Deploy/run the Centra platform | **GCSE** (+ On-Premise) | Certification ladder |
| Learn Akamai Cloud | **Cloud Computing Foundations Certification** | Certification (Foundational) |
| Deliver Akamai as a partner | **GCSP**, **Certified Partner: Solutions Architect** | Partner track |

**The Guardicore ladder is the one to treat as a real certification path** — it has levels, role splits, and exam depth the course badges do not, and it maps onto a genuine specialty (microsegmentation) with an existing hands-on lab in this encyclopedia. If your work is segmentation, GCSA → GCSA Advanced is the spine; everything else in the catalog is a course badge attesting attendance.

## Preparing

1. **The course is the credential for most badges** — enroll through Learn Akamai, attend the ILT/VILT, earn the Credly badge. Preparation is the course; there is no separate exam blueprint to study against for these.
2. **The certification tier (Guardicore, API Security, Cloud Foundations) has exams** — but their mechanics (duration, questions, passing score) are unpublished. Prepare from the badge skill lists (the closest thing to a blueprint), the product documentation, and, for Guardicore, **do [Volume XCV](../../volume-095-akamai-guardicore-lab/README.md)** — the hands-on build is the best preparation the encyclopedia can offer.
3. **Akamai Cloud has a free trial** and public TechDocs — the Cloud Foundations concepts are learnable hands-on at no cost.

> **The don't-assert rule, sixth vendor running:** no Akamai credential publishes exam duration, question count, or passing score. The badge metadata (level, Paid/Free, time band) is the ceiling of what is public. Any third-party source stating exam specifics is guessing.

## Where Akamai sits in the encyclopedia

Akamai touches three shelves, and its distinctive position is **breadth under one roof**:

| Shelf | Neighbors | Akamai's angle |
|:---|:---|:---|
| **Edge / CDN** | [CXLII Cloudflare](../../volume-142-cloudflare-certifications/README.md) | The enterprise incumbent: per-product depth, course-based enablement, quote-based pricing — versus Cloudflare's one-model self-serve platform |
| **Zero trust** | [XXXV Zscaler](../../volume-035-zscaler-zero-trust-exchange/README.md), [CXXVII Netskope](../../volume-127-netskope-certifications/README.md), [LXXXVII Microseg](../../volume-087-microsegmentation-options/README.md) | The rare vendor selling **both** north-south (EAA/SIA) **and** east-west (Guardicore) |
| **Cloud** | [XVII AWS](../../volume-017-aws-architecture-security/README.md), [XXXIII Azure](../../volume-033-microsoft-azure-certifications/README.md) | The latency/distribution specialist, not the everything-cloud |

The comparison to carry is **Akamai versus Cloudflare** (the Batch F edge volume), because they meet in every enterprise edge evaluation. Cloudflare's story is architectural uniformity and a free on-ramp; Akamai's is depth, breadth, and an enterprise relationship — and the credential programs are perfect miniatures of each: Cloudflare's two self-serve Associate exams versus Akamai's 192-badge issuer catalog spanning courses, certifications, partners, and internal awards. Neither program shape is better; each fits its company.

And the encyclopedia-specific note: Akamai is the only vendor whose **certification volume has a matching build-it-yourself lab volume** ([XCV](../../volume-095-akamai-guardicore-lab/README.md)) already shipped. For the Guardicore path, that pairing — concepts here, hands-on there — is the strongest study route in the whole series.

## Currency

- **Badges issue continuously.** Akamai University adds course deliveries year-round (the live schedule ran August through November at verification); the badge catalog grows steadily.
- **Acquisitions reshape the security lineup.** Guardicore (segmentation), Noname (API Security), and Linode (Cloud) are all acquisitions still being integrated into naming and credentials — the KSD → App & API Protector lineage in the badges is one visible seam. Expect the security-course names to keep shifting.
- **The certification URLs move.** `learn.akamai.com/certification` already redirects to TechDocs; anchor on the Akamai University: Customer Enablement page.
- **Verified 4 August 2026** from akamai.com (Akamai University: Customer Enablement — program, portfolio, live schedule, badge FAQ) and the Akamai Credly issuer catalog (192 badges: names, levels, cost flags, time bands, skill lists). Exam mechanics were not published and are asserted nowhere in this volume.

## Hands-On Lab

### Lab 9.1 — Build your Akamai path

**Objective:** Choose credentials by role and effort.

```bash
python3 - <<'EOF'
ROLE = {                              # hours/week
  "WAF / bot operations":           8,
  "web performance tuning":         5,
  "segmentation (Guardicore)":      9,
  "API security design":            4,
  "delivery config / property mgmt":6,
}
PATH = {
  "WAF / bot operations":           ("WAAP + Bot&Abuse course badges", "course"),
  "web performance tuning":         ("Web Perf Foundations + Offload",  "course"),
  "segmentation (Guardicore)":      ("GCSA -> GCSA Advanced",           "CERTIFICATION"),
  "API security design":            ("API Security - Architect",        "CERTIFICATION"),
  "delivery config / property mgmt":("Automation & DevOps course",      "course"),
}
total = sum(ROLE.values())
print(f"{'activity':32}{'h/wk':>6}   credential (type)")
for act, h in sorted(ROLE.items(), key=lambda kv: -kv[1]):
    cred, typ = PATH[act]
    print(f"{act:32}{h:>6}   {cred} ({typ})")
top = max(ROLE, key=ROLE.get)
print(f"\nBiggest slice: {top} ({ROLE[top]}/{total}h = {ROLE[top]/total*100:.0f}%).")
print(f"-> {PATH[top][0]} — and it is a CERTIFICATION, not a course badge.")
print("\nThe honest read: a Guardicore-heavy week should chase the real ladder")
print("(GCSA + Advanced) and treat the delivery/WAF course badges as useful")
print("attendance records alongside it. A DELIVERY-heavy week is the reverse —")
print("course badges are the right currency, and there is no deeper cert to chase.")
print("Match the credential TYPE to whether your specialty has an exam ladder.")
EOF
```

**Expected result:** A segmentation-heavy week pointing at the GCSA certification ladder, with delivery and WAF work correctly matched to course badges. The type-matching rule is the decision: some Akamai specialties have real exam ladders (Guardicore, API Security) and some only have course badges, and chasing a certification that does not exist for your specialty wastes the year.

**Negative test:** Collecting course badges as if they were certifications. They attest attendance; for a segmentation career, GCSA Advanced is the credential that says you can actually do the work.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 9.2 — The Guardicore study plan (with a real lab)

**Objective:** Assemble the one Akamai path with a hands-on build in this encyclopedia.

```bash
python3 - <<'EOF'
plan = """
TARGET: GCSA -> GCSA Advanced  (Akamai's deepest cert ladder; Intermediate -> Advanced)

BLUEPRINT SUBSTITUTE (badge skill lists — no formal exam blueprint published):
  GCSA:          Centra platform operation · flow map · labeling · policy ·
                 deception · DNS security · auditing · data retention
  GCSA Advanced: labeling SCHEMA · policy creation · ransomware mitigation ·
                 east-west traffic control · segmentation project planning ·
                 hands-on lab proficiency

STUDY (all free except the exam):
  [ ] read this volume's Chapter 07 (the why + the label discipline)
  [ ] DO VOLUME XCV — the 5-VM Guardicore build-it-yourself lab:
        [ ] stand up the flat network, PROVE lateral movement works
        [ ] map the flows (monitor-first)
        [ ] write LABEL-based policy, not address-based
        [ ] re-run the attack, MEASURE the blast-radius reduction
      (two tracks: real Centra console, or native nftables/WFP)
  [ ] read Guardicore/Centra TechDocs for platform specifics

MECHANICS — UNPUBLISHED:
  [ ] duration [ ] question count [ ] passing score — get from Akamai University,
      not from any third party. Enroll via Learn Akamai.

WHY THIS PATH: it is the only Akamai credential that is (a) a real exam ladder,
(b) a genuine specialty, and (c) paired with a hands-on lab already in this
encyclopedia. Chapter 07 concepts + Volume XCV build = the strongest prep the
series can give for any Akamai credential.
"""
print(plan)
print("Every checkbox is free but the exam. The Volume XCV lab is the differentiator —")
print("no other Akamai credential has a matching build in this series.")
EOF
```

**Expected result:** A Guardicore study plan built from badge skill lists and anchored on the Volume XCV hands-on build. The plan's value is the pairing — concepts in Chapter 07, the five-VM build in Volume XCV — which is the strongest preparation route the encyclopedia offers for any Akamai credential, and unique to this path.

**Negative test:** Preparing for GCSA from documentation alone. The Advanced credential lists "hands-on lab proficiency" as a skill; reading about segmentation does not build it, doing Volume XCV does.

**Rollback:** Keep the plan.

## Summary and Completion Checklist

- [ ] A credential path chosen by role, matching type (course badge vs certification) to specialty.
- [ ] The Guardicore ladder identified as Akamai's one real exam path, with API Security and Cloud beside it.
- [ ] Preparation built on course attendance, badge skill lists, TechDocs, and Volume XCV.
- [ ] Unpublished exam mechanics left unpublished.
- [ ] Akamai placed against Cloudflare (edge), the SSE/microseg shelf (zero trust), and the hyperscalers (cloud).
