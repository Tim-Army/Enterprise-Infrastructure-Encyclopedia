# Chapter 01: The ServiceNow Certification Program

## Learning Objectives

- Explain ServiceNow and the Now Platform.
- Describe the certification structure (CSA → CAD/CIS → CTA/CMA).
- Understand the exam model, prerequisites, and Personal Developer Instance.
- Map credentials to roles and plan a path.
- Verify current program facts from the authoritative source.

## Theory and Architecture

**ServiceNow** is an enterprise **digital-workflow platform** — the **Now Platform** — that started
in IT Service Management (ITSM) and now spans IT operations, security operations, customer service,
HR, and low-code application development, all on one data model and workflow engine. Its
certification program is large and tiered. The foundation is the **Certified System Administrator
(CSA)** — required (or strongly recommended) for almost every other credential — covering the
platform's core: tables, forms, lists, users/groups/**roles**, access control (**ACLs**), and basic
workflow. From there, two directions: the **Certified Application Developer (CAD)** for building on
the platform (server-side scripting, client scripts, REST APIs, scoped apps), and the large family of
**Certified Implementation Specialist (CIS)** credentials that each certify a **product area** (ITSM,
CSM, HR, Discovery, Event Management, Vulnerability Response, Security Incident Response, Risk &
Compliance, Strategic Portfolio Management, and more). At the top sit the **Certified Technical
Architect (CTA)** and **Certified Master Architect (CMA)** — experience-heavy, practical credentials.
Micro-certifications and new **Now Assist (GenAI)** credentials round it out. Exams are
**online-proctored**, and a **free Personal Developer Instance (PDI)** provides hands-on practice.

> **Scope.** ServiceNow administration is authorized platform work. The Security Operations content
> (Vulnerability Response, Security Incident Response) is **defensive** — orchestrating detection,
> prioritization, and response workflows on an authorized instance, never an attack.

## Design Considerations

Start with **CSA** — it gates the rest. Add **CAD** for development or a **CIS** for your product
area (ITSM is the most common). Pursue **CTA/CMA** with real implementation experience. Practice on a
**free PDI**. Verify current exams and prerequisites on servicenow.com — the platform releases twice
a year (named releases) and adds credentials (Now Assist/GenAI) frequently.

## Implementation and Automation

Confirm your practice environment (a free PDI and `python3` for modeling logic):

```bash
command -v python3 >/dev/null && echo "python3: ok" || echo "python3: install for labs"
echo "Request a free Personal Developer Instance at developer.servicenow.com for hands-on labs"
```

## Validation and Troubleshooting

The verified program facts (servicenow.com + ServiceNow community, 28 July 2026):

```text
Foundation: CSA (60Q/90min/$210) — prereq for CAD and CIS. Development: CAD. Implementation: CIS-* per product area (ITSM/CSM/HR/Discovery/Event Mgmt/VR/SIR/RC/SPM/...).
Architect: CTA (Certified Technical Architect), CMA (Certified Master Architect, multi-day practical). + Now Assist/GenAI micro-certs. Exams online-proctored. Free Personal Developer Instance (PDI).
```

Common pitfalls: attempting a **CIS/CAD** without the **CSA** prerequisite; and studying an old
**named release** (verify the current release on servicenow.com).

## Security and Best Practices

Build on the **CSA** foundation, choose **CAD or a CIS** for your role, and practice on a **free
PDI**, never a production instance. Treat Security Operations content as **defensive** workflow
orchestration. Verify current exams on servicenow.com.

## References and Knowledge Checks

- servicenow.com/services/training-and-certification and developer.servicenow.com: the program and PDI.
- ServiceNow Community certification blogs: the current, consolidated credential list.

**Knowledge checks**

1. What is the Now Platform?
2. Which certification is the prerequisite for most others?
3. What is a Personal Developer Instance?

## Hands-On Lab

Orientation walkthroughs. **Shared prerequisites for Labs 1.1–1.3** — a workstation with `python3`,
and (optionally) a free PDI, in a lab. **Cost:** none.

### Lab 1.1 — Map the platform and program

**Objective:** Learn the structure.

```python
python3 - <<'PY'
program={"CSA":"foundation (tables/ACLs/workflow) — prereq for the rest",
         "CAD":"application development (scripting, REST, scoped apps)",
         "CIS-*":"implementation specialist per product area (ITSM/CSM/HR/SecOps/...)",
         "CTA/CMA":"technical/master architect (experience + practical)"}
for cred,scope in program.items(): print(f"{cred:8}: {scope}")
PY
```

**Expected result:** the ServiceNow **credential structure** — the map this volume follows.

**Negative test:** assume any certification is a fine starting point; most require **CSA** first —
start there.

**Cleanup:** none.

### Lab 1.2 — Understand the exam model

**Objective:** Record the exam facts.

```python
python3 - <<'PY'
exam={"CSA":"60 questions, 90 minutes, ~$210","delivery":"online proctored",
      "prereq":"CSA for CAD and CIS","practice":"free Personal Developer Instance (PDI)",
      "release":"platform ships named releases ~twice a year (verify current)"}
for k,v in exam.items(): print(f"{k:9}: {v}")
PY
```

**Expected result:** the **exam model** and PDI — your scheduling reference.

**Negative test:** expect an in-person lab exam for CSA; it's **online-proctored** multiple-choice —
confirm the format on servicenow.com.

**Cleanup:** none.

### Lab 1.3 — Plan a certification path

**Objective:** Sequence credentials for a role.

```python
python3 - <<'PY'
paths={"Administrator":"CSA","Developer":"CSA -> CAD","ITSM consultant":"CSA -> CIS-ITSM",
       "SecOps":"CSA -> CIS-VR / CIS-SIR","Architect":"CSA -> CAD/CIS -> CTA -> CMA"}
for role,path in paths.items(): print(f"{role:16}: {path}")
PY
```

**Expected result:** role-to-path sequences — the ladder this volume follows.

**Negative test:** target **CTA** with no implementation experience; it expects it — build the track
first.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

ServiceNow certifies Now Platform practitioners from the CSA foundation through CAD and the CIS product
specializations to the CTA/CMA architect tiers, with Now Assist/GenAI micro-certs — online-proctored,
practiced on a free PDI, taught here as authorized platform administration.

- [ ] I can explain the Now Platform.
- [ ] I can describe the credential structure and CSA prerequisite.
- [ ] I can describe the exam model and PDI.
- [ ] I can plan a certification path.
- [ ] I completed Labs 1.1–1.3 including each negative test.
