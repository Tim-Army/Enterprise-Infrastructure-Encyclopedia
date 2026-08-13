# Chapter 01: The PSDGP Program

## Learning Objectives

- Explain what the Public Sector Data Governance Professional (PSDGP) credential certifies.
- Identify the certifying body (ICCP) and the training partners (R2C, Buchanan & Edwards).
- State the exam format, prerequisites, fee, and recertification model.
- Place PSDGP among ICCP's certification levels and the DGSP core body of knowledge.
- Verify current program facts from the authoritative sources.

## Theory and Architecture

The **Public Sector Data Governance Professional (PSDGP)** — also written CPSDGP — is a
certification issued by the **Institute for the Certification of Computing Professionals
(ICCP)**, the vendor-neutral body that certifies data and computing professionals. It is
delivered in partnership with **R2C (TheR2C)** and **Buchanan & Edwards**, who run the
preparation course. PSDGP certifies that a professional can **stand up and run a data
governance program specifically in a government (public-sector) context** — where overlapping
legacy systems, open-records obligations, privacy law, and records-retention mandates make
governance materially different from the commercial world.

The credential sits on top of ICCP's general data governance body of knowledge, the **Data
Governance and Stewardship Professional (DGSP)**. ICCP offers certifications at several
**levels** — Foundation, Associate/Practitioner, Mastery, and Principal — and PSDGP is the
public-sector specialization. Because it is process- and policy-oriented rather than
tool-oriented, the whole program is organized around **four content areas**: Mission Drivers,
Deliverables, Roles and Responsibilities, and the Legal and Regulatory Environment. Those four
areas are the exam blueprint and the spine of this volume (Chapters 02–05).

## Design Considerations

Treat PSDGP as a **program-building** credential, not a tool certification. The exam rewards
the ability to produce governance **deliverables** (charters, policies, catalogs, quality
frameworks, RACI models) and to align them with public-sector **mission drivers** and **law**.
Plan study around authoring real artifacts, not memorizing tool syntax.

## Implementation and Automation

Confirm the program facts from the source before you register:

```bash
curl -sSL -A "Mozilla/5.0" "https://www.ther2c.com/psdg" \
  | grep -oiE 'Mission Drivers|Deliverables|Roles and Responsibilities|Legal and Regulatory' \
  | sort -u
```

## Validation and Troubleshooting

The verified program facts (ther2c.com and iccp.org, 28 July 2026):

```text
Credential : Public Sector Data Governance Professional (PSDGP / CPSDGP)
Body       : ICCP; training via R2C (TheR2C) and Buchanan & Edwards
Exam       : 100 questions, 90 minutes, timed, proctored (third-party center)
Prereq     : Associate's (AA/AS) degree or higher AND >2 years experience,
             OR a 'core'-level ICCP certification (e.g., DGSP)
Fee        : certification fee; R2C 3-day course US$1,495 incl. exam
Validity   : 3 years, renewed via Continuing Professional Development (CPD)
Content    : Mission Drivers; Deliverables; Roles & Responsibilities; Legal & Regulatory
```

Common pitfalls: assuming commercial data governance transfers unchanged (public-sector
**law and records** obligations differ); and thinking the exam is technical (it is
**governance and policy**).

## Security and Best Practices

Public-sector governance carries statutory duties — **privacy, open records, records
retention, and security compliance**. Study the four content areas together: a deliverable
(a policy) exists to satisfy a mission driver and a legal obligation, and is executed by a
role. Keep every artifact traceable to a driver and a law.

## References and Knowledge Checks

- ther2c.com/psdg and iccp.org: the PSDGP course, ICCP certification, and DGSP body of knowledge.
- datagovernance.education (Buchanan & Edwards): the virtual course and ICCP exam.

**Knowledge checks**

1. Who certifies PSDGP, and who delivers the training?
2. What are the exam format and the prerequisites?
3. Name the four content areas.

## Hands-On Lab

Orientation walkthroughs. **Shared prerequisites for Labs 1.1–1.3** — a shell with `curl` and
`python3`. **Cost:** none.

### Lab 1.1 — Confirm the four content areas

**Objective:** Read the exam blueprint from the source.

```bash
curl -sSL -A "Mozilla/5.0" "https://www.ther2c.com/psdg" \
  | grep -oiE 'Mission Drivers|Deliverables|Roles and Responsibilities|Legal and Regulatory' \
  | sort -u
```

**Expected result:** the four content areas — **Mission Drivers, Deliverables, Roles and
Responsibilities, Legal and Regulatory** — the spine of the exam.

**Negative test:** study a commercial DAMA-DMBOK outline instead; PSDGP is scoped to the
**public sector** — confirm the four areas on ther2c.com.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 1.2 — Check your eligibility

**Objective:** Decide which prerequisite path applies.

```python
python3 - <<'PY'
def eligible(degree_aa_or_higher, years_experience, has_core_iccp_cert):
    path_a = degree_aa_or_higher and years_experience > 2
    path_b = has_core_iccp_cert
    return path_a or path_b, {"degree+exp": path_a, "core-cert": path_b}
ok, why = eligible(True, 3, False)
print("eligible:", ok, why)
PY
```

**Expected result:** `eligible: True {'degree+exp': True, 'core-cert': False}` — the
degree-plus-experience path qualifies; a core ICCP cert (DGSP) is the alternate.

**Negative test:** assume anyone may sit; PSDGP has an **education + experience** gate (or a
core-cert alternate) — check before registering.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 1.3 — Model the exam and recert

**Objective:** Record the exam and renewal mechanics.

```python
python3 - <<'PY'
exam={"questions":100,"minutes":90,"proctored":True,"membership_required":False}
recert={"validity_years":3,"method":"Continuing Professional Development (CPD)"}
print("exam:",exam)
print("recert:",recert)
print("pace (min/question):", round(exam["minutes"]/exam["questions"],2))
PY
```

**Expected result:** a 100-question/90-minute proctored exam (**0.9 min/question**) and a
3-year CPD renewal — your pacing and maintenance plan.

**Negative test:** plan to recertify by re-exam or CEUs; PSDGP renews through **CPD** — track
professional-development activity.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

PSDGP is ICCP's public-sector data governance credential, taught by R2C and Buchanan &
Edwards, examined in 100 questions over 90 minutes, gated by an education-plus-experience (or
core-cert) prerequisite, and renewed every three years through CPD. Its four content areas —
Mission Drivers, Deliverables, Roles and Responsibilities, and the Legal and Regulatory
Environment — organize the rest of this volume.

- [ ] I can state who certifies and who teaches PSDGP.
- [ ] I can state the exam format and prerequisites.
- [ ] I can name the four content areas.
- [ ] I can explain the 3-year CPD recertification.
- [ ] I completed Labs 1.1–1.3 including each negative test.
