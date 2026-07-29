# Chapter 01: The GIAC Certification Program

## Learning Objectives

- Explain what GIAC is and its relationship to SANS.
- Describe the eight GIAC focus areas.
- Understand CyberLive hands-on practical testing and the open-book, proctored exam model.
- Map credentials to focus areas and plan a path.
- Verify current program facts from the authoritative source.

## Theory and Architecture

**GIAC (Global Information Assurance Certification)**, owned by the **SANS Institute**, offers
**60-plus** technical cybersecurity certifications — among the most hands-on in the industry.
Credentials are organized into **eight focus areas**: **Cybersecurity & IT Essentials**, **Cyber
Defense**, **Offensive Operations**, **Digital Forensics and Incident Response (DFIR)**, **Cloud
Security**, **Industrial Control Systems (ICS) Security**, **Cybersecurity Leadership**, and a new
**Artificial Intelligence** area. Each certification aligns to a SANS course (SEC/FOR/LDR/ICS
numbers) but the course is **not required** to sit the exam. Exams are **proctored** (Pearson VUE
testing centers or remote proctoring) and **open-book** (candidates bring a printed index and
references), and many include **CyberLive** — **hands-on practical testing** where the candidate
performs real tasks on live virtual machines with actual tools, not just multiple-choice questions.
Certifications are valid for **four years** and are renewed through continuing education or
re-examination. This volume teaches each focus area with hands-on, **defensive** labs — the
offensive tracks are taught strictly as **authorized, educational assessment methodology**.

> **Scope.** Every lab in this volume is **defensive or authorized** — detection, monitoring,
> forensics, incident response, hardening, and *authorized* assessment methodology (scope, rules of
> engagement, safe local commands). No lab is an operational attack against a system you do not own.

## Design Considerations

Choose a **focus area** that matches your role: Cyber Defense and DFIR for blue teams, Offensive
Operations for authorized red teams, Cloud/ICS for those domains, Leadership for managers. Prefer
**CyberLive** certifications for hands-on validation. Budget for the **four-year** renewal. Verify
current codes and course alignment on giac.org — the program adds certifications frequently
(recent AI additions).

## Implementation and Automation

Confirm your practice toolset is present (used throughout the volume):

```bash
for t in python3 tcpdump tshark jq; do command -v "$t" >/dev/null && echo "$t: ok" || echo "$t: install for labs"; done
```

## Validation and Troubleshooting

The verified program facts (giac.org focus-area pages, 28 July 2026):

```text
GIAC = SANS-owned, ~62 certs across 8 focus areas: Essentials, Cyber Defense, Offensive Operations,
DFIR, Cloud Security, ICS Security, Leadership, Artificial Intelligence.
Exams: proctored + open-book; many use CyberLive (hands-on practical on live VMs). Validity: 4 years.
Course-aligned (SEC/FOR/LDR/ICS) but course not required. Codes start with G (GSEC, GCIH, GCFA, ...).
```

Common pitfalls: assuming a GIAC exam is multiple-choice only (many are **CyberLive** practical);
and thinking a SANS course is mandatory (the **exam** is the credential).

## Security and Best Practices

Learn the **current** focus areas and codes on giac.org, prefer **CyberLive** certs for real skills,
practice on authorized lab systems, and treat offensive material as **authorized methodology** only.
Renew before the four-year expiry. Third-party dumps are neither authoritative nor permitted.

## References and Knowledge Checks

- giac.org/certifications and the focus-area pages: the program, codes, and CyberLive.
- sans.org: the aligned courses and roadmaps.

**Knowledge checks**

1. What is GIAC's relationship to SANS?
2. Name four of the eight focus areas.
3. What is CyberLive?

## Hands-On Lab

Orientation walkthroughs. **Shared prerequisites for Labs 1.1–1.3** — a Linux workstation with
`python3` and `jq`, in a lab. **Cost:** none.

### Lab 1.1 — Inventory the focus areas

**Objective:** Record the eight focus areas.

```python
python3 - <<'PY'
areas=["Cybersecurity & IT Essentials","Cyber Defense","Offensive Operations",
       "Digital Forensics & Incident Response","Cloud Security","ICS Security",
       "Cybersecurity Leadership","Artificial Intelligence"]
for i,a in enumerate(areas,1): print(f"{i}. {a}")
PY
```

**Expected result:** the **eight focus areas** — the map this volume follows.

**Negative test:** try to list them from memory of a single vendor; GIAC spans **defense, offense,
forensics, cloud, ICS, leadership, and AI** — use the focus-area structure.

**Cleanup:** none.

### Lab 1.2 — Map credentials to focus areas

**Objective:** Build a code reference.

```python
python3 - <<'PY'
m={"Essentials":["GFACT","GISF","GSEC"],
   "Cyber Defense":["GCIA","GMON","GCDA","GDSA","GDAT"],
   "Offensive":["GPEN","GWAPT","GXPN","GMOB","GEVA"],
   "DFIR":["GCIH","GCFA","GNFA","GREM","GCTI"],
   "Cloud":["GCLD","GCSA","GCFR","GWEB"],
   "ICS":["GICSP","GRID","GCIP"],
   "Leadership":["GSLC","GSTRT","GSOM","GCCC"],
   "AI":["GMLE","GAIPS","GASAE","GOAA"]}
for area,codes in m.items(): print(f"{area:12}: {', '.join(codes)}")
PY
```

**Expected result:** a focus-area → code map — your scheduling reference.

**Negative test:** guess a code's meaning from letters alone (e.g., GX-* are **experienced**
practical exams); confirm each on giac.org.

**Cleanup:** none.

### Lab 1.3 — Plan a certification path

**Objective:** Sequence credentials for a role.

```python
python3 - <<'PY'
paths={"Blue team analyst":"GSEC -> GCIH -> GCIA -> GCDA/GMON",
       "DFIR":"GCIH -> GCFA -> GNFA -> GREM",
       "Authorized red team":"GSEC -> GPEN -> GWAPT -> GXPN",
       "Cloud security":"GSEC -> GCLD -> GCSA -> GCFR",
       "Leadership":"GSLC -> GSTRT -> GSOM"}
for role,path in paths.items(): print(f"{role:20}: {path}")
PY
```

**Expected result:** role-to-path sequences — the ladder this volume follows.

**Negative test:** start at an **experienced/expert** exam (GXPN, GX-*) with no foundation; build up
from **GSEC/GFACT** — climb the path.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

GIAC, owned by SANS, offers 60-plus certifications across eight focus areas, delivered as proctored,
open-book exams — many with CyberLive hands-on practical testing — valid four years. This volume
teaches each area defensively, with offensive tracks framed as authorized methodology.

- [ ] I can explain GIAC's relationship to SANS.
- [ ] I can name the eight focus areas.
- [ ] I can describe CyberLive and the exam model.
- [ ] I can map credentials to focus areas and plan a path.
- [ ] I completed Labs 1.1–1.3 including each negative test.
