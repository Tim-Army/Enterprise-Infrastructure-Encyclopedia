# Chapter 01: The ISC2 Certification Program

## Learning Objectives

- Explain what ISC2 is and why its credentials sit at the governance and architecture tier above the vendor and CompTIA tracks.
- Describe the ISC2 credential ladder: CC, SSCP, CISSP, CCSP, CGRC, CSSLP, and the CISSP concentrations.
- Explain the experience requirement, endorsement, and the Associate of ISC2 path.
- Describe the exam experience: Pearson VUE, Computer Adaptive Testing (CAT), and the 700/1000 pass mark.
- Explain the Continuing Professional Education (CPE) and Annual Maintenance Fee (AMF) renewal model and the ISC2 Code of Ethics.

## Theory and Architecture

**ISC2** — the International Information System Security Certification
Consortium, historically styled **(ISC)²** — is the non-profit body behind the
**vendor-neutral** advanced security certifications, most famously the
**CISSP**. Where CompTIA validates foundational, hands-on skill domains and the
vendor tracks (Cisco, Palo Alto, Fortinet, Zscaler, the cloud providers)
validate implementation on specific products, ISC2 credentials validate the
**management, architecture, engineering, and governance** of security programs.
That is why ISC2 sits *above* the other tracks in this encyclopedia: a Security+
holder implements a control; a CISSP decides which control, why, and how it fits
the organization's risk posture, law, and lifecycle.

The program is a **ladder by experience and role**, not a set of parallel silos:

- **Certified in Cybersecurity (CC)** — the entry credential; **no experience
  required**, and the exam is free under the ISC2 "One Million Certified in
  Cybersecurity" initiative.
- **Systems Security Certified Practitioner (SSCP)** — hands-on security
  operations; **one year** of experience.
- **Certified Information Systems Security Professional (CISSP)** — the
  flagship, "the world's leading cybersecurity certification"; **five years**
  across two or more of its eight domains.
- **CISSP concentrations** — **ISSAP** (architecture), **ISSEP** (engineering),
  **ISSMP** (management); each requires the **CISSP plus two years**.
- **Certified Cloud Security Professional (CCSP)** — cloud security architecture
  and operations; **five years** (co-created with the Cloud Security Alliance).
- **Certified in Governance, Risk and Compliance (CGRC)** — the authorization
  and RMF credential (formerly **CAP**); **two years**.
- **Certified Secure Software Lifecycle Professional (CSSLP)** — secure software
  development across the SDLC; **four years**.

Every ISC2 credential requires agreement to the **ISC2 Code of Ethics**,
professional **endorsement** by an existing member after passing, and ongoing
membership. A candidate who passes but lacks the experience becomes an
**Associate of ISC2** and has a defined window (for example, up to six years for
CISSP) to earn the experience.

## Design Considerations

Choose an ISC2 path by **role and seniority**. A newcomer or career-changer
starts at **CC** to enter the field with credibility. A working analyst or
administrator in a hands-on security-operations role targets **SSCP**. The
**CISSP** is the pivot point: it is the credential most demanded for security
engineer, manager, and architect roles, and it unlocks the three
**concentrations** for those who specialize in **architecture (ISSAP)**,
**engineering (ISSEP)**, or **management (ISSMP)**. Specialists branch to
**CCSP** for cloud, **CGRC** for authorization and compliance, and **CSSLP** for
application security.

Plan for the **non-exam requirements** early. Unlike CompTIA, ISC2 enforces
**experience**, requires **endorsement**, and binds holders to a **Code of
Ethics** whose violation can revoke a credential. Budget for the **Annual
Maintenance Fee** and the **CPE** obligation from day one — an ISC2 credential
is a multi-year professional commitment, not a one-time exam.

## Implementation and Automation

ISC2 publishes an authoritative **Exam Outline** (the blueprint) for every
credential, each with **weighted domains** and an **effective date**. The
outlines are the single source of truth for what an exam covers and are updated
on a **Job Task Analysis** cycle — verify the current outline and its effective
date before studying:

```bash
# The exam-outline hub lists the current outline (and effective date) per credential
curl -sSL -A "Mozilla/5.0" "https://www.isc2.org/certifications/exam-outlines" \
  | grep -oiE '(CISSP|CCSP|SSCP|CGRC|CSSLP|ISSAP|ISSEP|ISSMP|Certified in Cybersecurity)' \
  | sort -u
```

Domain **names** and **weights** are facts you can plan against; ISC2's detailed
sub-objective text is copyrighted study material — read it from the official
outline, do not redistribute it.

## Validation and Troubleshooting

Confirm a credential's blueprint, exam mechanics, and status on its outline:

```text
isc2.org > Certifications > open the credential > "Exam Outline":
  - the weighted domains and the effective date
  - number of items, duration, and format (CAT vs linear)
  - the 700/1000 passing score
  - experience requirement and endorsement
```

Common pitfalls: studying a **superseded outline** (the CISSP refreshed 15 April
2024, SSCP September 2024, and the concentrations **ISSAP/ISSEP/ISSMP** were all
rewritten effective **1 August 2025** — with new domain counts); assuming the
old name (**CAP** is now **CGRC**; the styling **(ISC)²** is now **ISC2**);
treating **CC** as a career credential rather than the entry gateway; and
forgetting that passing is only step one — **endorsement**, **experience**, and
the **AMF** must all be satisfied to be certified.

## Security and Best Practices

Verify every fact on **isc2.org**, never a brain-dump site — dumps violate the
**ISC2 Code of Ethics** and the exam agreement and can permanently revoke a
credential. Use official ISC2 training and the **Official Study Guides** and
practice tests. Track **CPE** continuously (record credits as you earn them, not
at renewal) and pay the **AMF** on time so a credential does not lapse. For
teams, map roles to the ISC2 ladder — CISSP for architects and managers, CCSP
for cloud, CSSLP for developers, CGRC for authorization staff — and note that
several ISC2 credentials satisfy **DoD 8140/8570** IAT/IAM/IASAE baselines.

## References and Knowledge Checks

- isc2.org: *Certifications* overview; *Exam Outlines* hub; individual credential pages; *Code of Ethics*; *CPE Handbook*.

**Knowledge checks**

1. Why do ISC2 credentials sit above CompTIA and the vendor tracks in this encyclopedia?
2. What are the four things (beyond passing the exam) required to become and stay ISC2-certified?
3. What is the Associate of ISC2, and when does it apply?

## Hands-On Lab

Exam-preparation walkthroughs for reading and verifying the ISC2 program.

**Shared prerequisites for Labs 1.1–1.3** — a Linux shell with `curl` and
`python3`. **Cost:** none.

### Lab 1.1 — Enumerate the ISC2 credential ladder (Topic: Read the program)

**Objective:** List the current credentials from the authoritative source.

```bash
curl -sSL -A "Mozilla/5.0" "https://www.isc2.org/certifications" \
  | grep -oiE '\b(CC|SSCP|CISSP|CCSP|CGRC|CSSLP|ISSAP|ISSEP|ISSMP)\b' \
  | sort -u
```

**Expected result:** the nine credentials of the ladder — `CC`, `SSCP`,
`CISSP`, `CCSP`, `CGRC`, `CSSLP`, and the concentrations `ISSAP`, `ISSEP`,
`ISSMP` — the whole program in one view.

**Negative test:** rely on an old blog that still lists `CAP` or `HCISPP`; CAP
was renamed **CGRC** and HCISPP is retired — use the live catalog.

**Cleanup:** none.

### Lab 1.2 — Map a credential to its experience requirement (Topic: Plan the path)

**Objective:** Model the experience gate that ISC2 enforces.

```bash
python3 - <<'PY'
req = {"CC":0, "CGRC":2, "SSCP":1, "CSSLP":4, "CISSP":5, "CCSP":5,
       "ISSAP":"CISSP+2", "ISSEP":"CISSP+2", "ISSMP":"CISSP+2"}
for k in ["CC","SSCP","CGRC","CSSLP","CISSP","CCSP","ISSAP","ISSEP","ISSMP"]:
    print(f"{k:6} -> {req[k]} years")
PY
```

**Expected result:** CC needs 0, SSCP 1, CGRC 2, CSSLP 4, CISSP and CCSP 5, and
the concentrations require the CISSP plus 2 — the ladder ISC2 enforces.

**Negative test:** assume experience is waived if you pass; without it you are an
**Associate of ISC2**, not certified.

**Cleanup:** none.

### Lab 1.3 — Confirm an exam outline's effective date (Topic: Verify currency)

**Objective:** Prove which outline version is current before you study.

```bash
curl -sSL -A "Mozilla/5.0" \
  "https://www.isc2.org/certifications/cissp/cissp-certification-exam-outline" \
  | grep -oiE 'Effective[^<]{0,40}20[0-9]{2}' | head -1
```

**Expected result:** the CISSP outline's effective date (the current refresh
took effect **15 April 2024**) — always study the current blueprint.

**Negative test:** study a 2021-era CISSP outline; the domain weights changed in
the 2024 refresh — confirm the effective date first.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

ISC2 is the vendor-neutral governance, architecture, and management tier of the
security profession. Its credentials form an experience-gated ladder — CC,
SSCP, CISSP (with the ISSAP/ISSEP/ISSMP concentrations), CCSP, CGRC, and CSSLP —
each requiring the Code of Ethics, endorsement, CPE, and an Annual Maintenance
Fee. Exams run on Pearson VUE, CISSP and others via Computer Adaptive Testing,
with a 700/1000 pass mark and weighted, dated exam outlines.

- [ ] I can place ISC2 in the encyclopedia's certification stack.
- [ ] I can name the nine credentials and their experience gates.
- [ ] I can explain endorsement, the Associate of ISC2, and the AMF.
- [ ] I can verify a current exam outline and its effective date.
- [ ] I completed Labs 1.1–1.3 including each negative test.
