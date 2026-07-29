# Chapter 01: The Tenable Certification Program

## Learning Objectives

- Explain Tenable's role in vulnerability and exposure management.
- Describe the three current product certifications.
- Understand the two-part (written + practical) exam model and validity.
- Map credentials to products and plan a path.
- Verify current program facts from the authoritative source.

## Theory and Architecture

**Tenable** is the vulnerability- and exposure-management leader — creator of the **Nessus** scanner
and the broader **Tenable One** exposure-management platform. Its certification program is
**product-based**, currently validating three solutions: the **Tenable One Vulnerability Management
Certification** (Tenable Vulnerability Management — cloud VM), the **Tenable Security Center
Certification** (the on-premises console), and the **Tenable One OT Exposure Certification** (Tenable
OT Security). Each exam is **two parts**: a **written** exam (60 multiple-choice questions, 120
minutes, 80% to pass) and a hands-on **practical** exam (up to 30 tasks, 240 minutes, 80% to pass),
both delivered **online with proctoring** (government photo ID required; the practical permits access
to the pyTenable/developer API documentation). Certifications are valid **two years**, renewed by
retaking both parts. The program validates the ability to **plan, deploy, verify, and troubleshoot**
the platform. Because vulnerability and exposure management exist to **find and fix weaknesses before
attackers do**, this entire volume is defensive.

> **Scope.** Vulnerability and exposure management is a defensive discipline. Every lab is
> **authorized administration** — scanning, prioritizing, and remediating on systems you are
> authorized to assess — never an attack. Scan only assets you own or are authorized to scan.

## Design Considerations

Choose the certification matching your product: **Vulnerability Management** for cloud VM, **Security
Center** for on-prem, **OT Exposure** for operational technology. Prepare for **both** exam parts —
the practical rewards real hands-on skill. Budget for the **two-year** renewal. Verify current exams
on tenable.com — the platform is consolidating under **Tenable One** exposure management.

## Implementation and Automation

Confirm your practice toolset (used throughout the volume):

```bash
command -v python3 >/dev/null && echo "python3: ok" || echo "python3: install for labs"
echo "Practice with a Nessus Essentials (free) scanner and authorized lab targets only"
```

## Validation and Troubleshooting

The verified program facts (tenable.com/education/certification-program, 28 July 2026):

```text
Three certifications: Tenable One Vulnerability Management, Tenable Security Center, Tenable One OT Exposure.
Exam = two parts: written (60 MCQ, 120 min, 80%) + practical (up to 30 tasks, 240 min, 80%). Online proctored. Valid 2 years.
Products: Nessus, Tenable Vulnerability Management, Security Center, Web App Scanning, Cloud Security, OT Security, Tenable One.
```

Common pitfalls: preparing only for the **written** part and failing the **practical**; and scanning
**unauthorized** assets (always scan only what you own/are authorized to assess).

## Security and Best Practices

Learn the **current** certifications and platform on tenable.com, prepare for **both** exam parts,
and practice on **authorized** targets only (Nessus Essentials + your own lab). Renew before the
two-year expiry. Third-party dumps are neither authoritative nor permitted.

## References and Knowledge Checks

- tenable.com/education/certification-program: the certifications and exam model.
- docs.tenable.com and pytenable.readthedocs.io: product and API documentation.

**Knowledge checks**

1. What does Tenable's platform do?
2. Name the three current certifications.
3. What are the two parts of each exam?

## Hands-On Lab

Orientation walkthroughs. **Shared prerequisites for Labs 1.1–1.3** — a workstation with `python3`,
in a lab. **Cost:** none.

### Lab 1.1 — Map the products to certifications

**Objective:** Match certs to products.

```python
python3 - <<'PY'
certs={"Tenable One Vulnerability Management":"Tenable Vulnerability Management (cloud VM)",
       "Tenable Security Center":"on-prem console (Tenable.sc)",
       "Tenable One OT Exposure":"Tenable OT Security"}
for c,p in certs.items(): print(f"{c:38}: {p}")
print("Also across the platform: Nessus, Web App Scanning, Cloud Security, Tenable One")
PY
```

**Expected result:** the three certifications mapped to their **products** — the map this volume
follows.

**Negative test:** assume one Tenable cert covers everything; each targets a **specific product** —
pick the one for your platform.

**Cleanup:** none.

### Lab 1.2 — Understand the two-part exam

**Objective:** Record the exam structure.

```python
python3 - <<'PY'
exam={"Written":"60 MCQ, 120 min, 80% to pass","Practical":"up to 30 tasks, 240 min, 80% to pass",
      "Delivery":"online, proctored (gov photo ID)","Validity":"2 years (retake both to recertify)"}
for k,v in exam.items(): print(f"{k:10}: {v}")
PY
```

**Expected result:** the **written + practical** structure and validity — your scheduling reference.

**Negative test:** expect a single multiple-choice exam; Tenable requires a **hands-on practical**
too — prepare for both.

**Cleanup:** none.

### Lab 1.3 — Plan a certification path

**Objective:** Sequence credentials for a role.

```python
python3 - <<'PY'
paths={"Cloud VM analyst":"Tenable One Vulnerability Management",
       "On-prem VM engineer":"Tenable Security Center",
       "OT security":"Tenable One OT Exposure",
       "Exposure management lead":"VM + OT + Tenable One platform breadth"}
for role,path in paths.items(): print(f"{role:26}: {path}")
PY
```

**Expected result:** role-to-path choices — the certifications this volume follows.

**Negative test:** pursue OT Exposure for a pure cloud-VM role; match the cert to your **product and
role**.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Tenable certifies vulnerability- and exposure-management practitioners across three product
certifications (Vulnerability Management, Security Center, OT Exposure), each a two-part written +
practical exam, valid two years — taught here as defensive scanning, prioritization, and remediation.

- [ ] I can explain what Tenable does.
- [ ] I can name the three certifications.
- [ ] I can describe the two-part exam.
- [ ] I can plan a certification path.
- [ ] I completed Labs 1.1–1.3 including each negative test.
