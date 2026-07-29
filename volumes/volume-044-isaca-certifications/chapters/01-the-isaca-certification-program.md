# Chapter 01: The ISACA Certification Program

## Learning Objectives

- Explain what ISACA certifies and how it complements ISC2 in the governance stack.
- Describe the credential map: the classic certifications, CCOA, the Advanced in AI family, and CMMC roles.
- Explain job-practice domains, the exam experience, and the CPE maintenance model.
- Understand experience requirements and endorsement/verification.
- Verify a current exam content outline from the authoritative source.

## Theory and Architecture

**ISACA** (historically the Information Systems Audit and Control Association) is
the professional body behind the world's leading **audit, governance, and risk**
certifications. Where ISC2 (Volume XL) certifies security architecture,
engineering, and management, ISACA owns the **audit and governance** quadrant:
its flagship **CISA** is the benchmark for IS auditors, **CISM** for security
managers, **CRISC** for risk practitioners, **CGEIT** for enterprise IT
governance, and **CDPSE** for data-privacy engineering. Together with ISC2, ISACA
completes the vendor-neutral governance-and-management tier that sits *above* the
CompTIA and vendor tracks.

The program spans several lines:

- **Classic certifications** — **CISA**, **CISM**, **CRISC**, **CGEIT**, and
  **CDPSE**, each built on a **job-practice analysis** with weighted domains.
- **CCOA** — **Certified Cybersecurity Operations Analyst**, a newer, **hands-on**
  credential (a hybrid exam with performance-based labs) for SOC analysts.
- **Advanced in AI family** — **AAIA** (AI Audit), **AAISM** (AI Security
  Management), and **AAIR** (AI Risk), new advanced credentials that extend CISA,
  CISM, and CRISC into AI governance.
- **CMMC ecosystem roles** — ISACA administers the **CMMC** assessor credentials
  (CCP, CCA, LCCA, CCI), plus a broad catalog of **certificates** (COBIT, IT
  Audit/Risk Fundamentals, AI Fundamentals, and more).

Certifications require relevant **work experience** (verified after passing) and
are maintained with **Continuing Professional Education (CPE)** credits and an
**annual maintenance fee** over a three-year cycle.

## Design Considerations

Choose an ISACA credential by **function**: auditors take **CISA**, security
leaders **CISM**, risk professionals **CRISC**, governance/board-facing roles
**CGEIT**, and privacy engineers **CDPSE**; SOC analysts who want a hands-on
credential take **CCOA**. The **Advanced in AI** trio is for professionals whose
audit, security-management, or risk work now spans **AI systems** — each extends
the corresponding base discipline. Plan for the **experience requirement** and
the ongoing **CPE** commitment from the start; like ISC2, an ISACA credential is
a multi-year professional membership, not a one-time exam.

## Implementation and Automation

ISACA publishes an **exam content outline** for every certification with weighted
**job-practice domains** — the authoritative blueprint. Confirm the current
outline and its weights before studying:

```bash
# Each certification's exam content outline carries its weighted domains
curl -sSL -A "Mozilla/5.0" \
  "https://www.isaca.org/credentialing/cisa/cisa-exam-content-outline" \
  | grep -oiE 'Domain [0-9][^<]{0,60}[0-9]{1,2}%' | head
```

Domain **names and weights** are facts you can plan against; ISACA's detailed
task and knowledge statements are copyrighted study material.

## Validation and Troubleshooting

Confirm a credential's blueprint and mechanics on its exam content outline:

```text
isaca.org > Credentialing > open the credential > "Exam Content Outline":
  - the weighted job-practice domains
  - number of questions and exam duration
  - experience requirement and CPE maintenance
```

Common pitfalls: studying a **superseded outline** (CDPSE moved from three to
four domains on 2 June 2025, and CRISC was updated in 2025); assuming the
**Advanced in AI** credentials are certificates (they are certifications that
extend the base certs); and forgetting that passing is only step one —
**experience verification** and **CPE** are required to certify and stay
certified.

## Security and Best Practices

Verify facts on **isaca.org**, never a dump site. Use ISACA's official review
materials and the **QAE** (questions/answers/explanations) databases. Track
**CPE** continuously and pay the annual maintenance fee so a credential does not
lapse. For teams, map roles to the ISACA quadrant — CISA for audit, CISM for
security management, CRISC for risk, CGEIT for governance, CDPSE for privacy —
and note ISACA's alignment with **COBIT**, **NIST**, and the **CMMC** ecosystem.

## References and Knowledge Checks

- isaca.org: *Credentialing* overview; per-credential *Exam Content Outline*; the CPE policy; COBIT.

**Knowledge checks**

1. How does ISACA's coverage complement ISC2's in the governance stack?
2. What are the five classic ISACA certifications and their functions?
3. What must be satisfied beyond passing the exam to become certified?

## Hands-On Lab

Exam-preparation walkthroughs for reading and verifying the ISACA program.

**Shared prerequisites for Labs 1.1–1.3** — a Linux shell with `curl` and
`python3`. **Cost:** none.

### Lab 1.1 — Enumerate the credential map (Topic: Read the program)

**Objective:** List the certifications from the authoritative source.

```bash
curl -sSL -A "Mozilla/5.0" "https://www.isaca.org/credentialing" \
  | grep -oiE '\b(CISA|CISM|CRISC|CGEIT|CDPSE|CCOA|AAIA|AAISM|AAIR)\b' \
  | sort -u
```

**Expected result:** the ISACA credentials — the classic five plus **CCOA** and
the Advanced in AI trio (**AAIA**, **AAISM**, **AAIR**) — the whole program in
one view.

**Negative test:** rely on an old chart that lists only CISA/CISM/CRISC/CGEIT/
CDPSE; it misses **CCOA** and the AI family — use the live catalog.

**Cleanup:** none.

### Lab 1.2 — Map a credential to its function (Topic: Plan the path)

**Objective:** Model the ISACA quadrant by function.

```bash
python3 - <<'PY'
fn = {"CISA":"audit","CISM":"security management","CRISC":"risk","CGEIT":"governance",
      "CDPSE":"data privacy","CCOA":"security operations (hands-on)",
      "AAIA":"AI audit","AAISM":"AI security mgmt","AAIR":"AI risk"}
for k,v in fn.items(): print(f"{k:6} -> {v}")
PY
```

**Expected result:** each credential mapped to its function — the role-to-cert
map that guides an ISACA path.

**Negative test:** treat CISA and CISM as interchangeable; audit (CISA) and
security management (CISM) are distinct disciplines — match the cert to the role.

**Cleanup:** none.

### Lab 1.3 — Confirm a current exam content outline (Topic: Verify currency)

**Objective:** Prove which outline (and weights) are current before studying.

```bash
curl -sSL -A "Mozilla/5.0" \
  "https://www.isaca.org/credentialing/cdpse/cdpse-exam-content-outline" \
  | grep -oiE 'Domain [0-9][^<]{0,60}[0-9]{1,2}%' | head
```

**Expected result:** CDPSE's **four** weighted domains (the June 2025 refresh) —
proof of the current structure, not the retired three-domain version.

**Negative test:** study a three-domain CDPSE guide; the outline changed in 2025
— confirm the current domains first.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

ISACA is the vendor-neutral **audit, governance, and risk** body that completes
the governance tier beside ISC2. Its program spans the classic certifications
(CISA, CISM, CRISC, CGEIT, CDPSE), the hands-on CCOA, the new Advanced in AI
family (AAIA, AAISM, AAIR), and the CMMC roles — each built on weighted
job-practice domains and maintained with experience verification and CPE.

- [ ] I can place ISACA beside ISC2 in the governance stack.
- [ ] I can name the classic five, CCOA, and the AI family and their functions.
- [ ] I can explain experience verification and CPE maintenance.
- [ ] I can verify a current exam content outline and its weights.
- [ ] I completed Labs 1.1–1.3 including each negative test.
