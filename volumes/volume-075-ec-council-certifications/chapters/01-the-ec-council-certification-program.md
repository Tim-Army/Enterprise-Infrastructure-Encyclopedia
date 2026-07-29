# Chapter 01: The EC-Council Certification Program

## Learning Objectives

- Explain EC-Council's role and its flagship CEH v13 certification.
- Describe the certification tracks and the ECC/iLabs exam model.
- Understand the ANSI accreditation and US DoD 8140 alignment.
- Map credentials to tracks and plan an authorized, defensive path.
- Verify current program facts from the authoritative source.

## Theory and Architecture

**EC-Council** (the International Council of E-Commerce Consultants) is a global cybersecurity
certification body best known for the **Certified Ethical Hacker (CEH)** — now at **v13, "with the
power of AI."** CEH validates **authorized, ethical** assessment: the exam is a **4-hour, 125
multiple-choice** knowledge test on the ECC exam portal covering 20 modules, and an optional
**6-hour, 20-challenge practical** in the **iLabs Cyber Range** earns the higher **CEH Master**.
Around CEH, EC-Council offers tracks for **penetration testing** (CPENT, WAHS, LPT Master),
**network defense** (CND, ICS/SCADA), **digital forensics** (CHFI), **SOC/incident/threat
intelligence** (CSA, ECIH, CTIA), **cloud/DevSecOps/application security** (CCSE, ECDE, CASE, ECES),
**executive** (CCISO), a new **AI Security & Management** family (CAIPM, COASP, CRAGE, AI Essentials),
and **foundations** (CCT, CSCU, ECSS, and the free-to-learn Essentials series). EC-Council programs
are **ANSI 17024** accredited, and CEH/CND/CHFI meet **US DoD 8140/8570** baseline requirements. This
volume teaches every track as **authorized, defensive** work — ethical-hacking material is paired
with countermeasures, and assessment is always gated on authorization and scope.

> **Scope.** EC-Council's "ethical hacking" and penetration-testing content is **authorized,
> educational methodology only**. Every lab is defensive (hardening, detection, forensics, response)
> or authorized assessment (scope, rules of engagement, safe local commands) — never an operational
> attack.

## Design Considerations

Choose a track by role: **CEH** for authorized assessment fundamentals, **CND** for defenders,
**CHFI** for forensics, **CSA/ECIH/CTIA** for SOC/IR, **CCISO** for leadership. Note **DoD 8140**
alignment if you work in that space. Prefer **practical** credentials (CEH Master, CPENT/LPT) for
hands-on proof. Verify current versions on eccouncil.org — CEH advances versions (v13 added AI).

## Implementation and Automation

Confirm your practice toolset (used throughout the volume):

```bash
for t in python3 nmap tcpdump tshark jq openssl; do command -v "$t" >/dev/null && echo "$t: ok" || echo "$t: install for labs"; done
```

## Validation and Troubleshooting

The verified program facts (eccouncil.org, 28 July 2026):

```text
Flagship: CEH v13 (with AI) — 4h/125 MCQ knowledge exam (ECC portal); CEH Practical 6h/20 iLabs challenges -> CEH Master.
Tracks: Ethical Hacking (CEH), PenTest (CPENT/WAHS/LPT), Network Defense (CND/ICS-SCADA), Forensics (CHFI),
  SOC/IR/Intel (CSA/ECIH/CTIA), Cloud/DevSecOps/AppSec (CCSE/ECDE/CASE/ECES), Executive (CCISO), AI Security (CAIPM/COASP/CRAGE),
  Foundations (CCT/CSCU/ECSS + Essentials NDE/EHE/DFE...). ANSI 17024 accredited; CEH/CND/CHFI meet US DoD 8140/8570.
```

Common pitfalls: treating CEH as license to attack (it is **authorized** assessment only); and
studying an old CEH version (confirm **v13** on eccouncil.org).

## Security and Best Practices

Learn the **current** versions and tracks on eccouncil.org, pursue **practical** credentials for real
skill, and treat all offensive material as **authorized methodology plus countermeasures**. Honor
DoD 8140 alignment where relevant. Third-party dumps are neither authoritative nor permitted.

## References and Knowledge Checks

- eccouncil.org/train-certify: the tracks, CEH v13, and exam model.
- ANSI and US DoD 8140 references: accreditation and baseline alignment.

**Knowledge checks**

1. What is EC-Council's flagship certification and its current version?
2. How does CEH Master differ from CEH?
3. Which EC-Council certs meet US DoD 8140 baseline?

## Hands-On Lab

Orientation walkthroughs. **Shared prerequisites for Labs 1.1–1.3** — a Linux workstation with
`python3`, in a lab. **Cost:** none.

### Lab 1.1 — Inventory the tracks

**Objective:** Record the certification tracks.

```python
python3 - <<'PY'
tracks={"Ethical Hacking":["CEH v13","CEH Master"],"PenTest":["CPENT","WAHS","LPT Master"],
        "Network Defense":["CND","ICS/SCADA"],"Forensics":["CHFI"],
        "SOC/IR/Intel":["CSA","ECIH","CTIA"],"Cloud/DevSecOps/AppSec":["CCSE","ECDE","CASE","ECES"],
        "Executive":["CCISO"],"AI Security":["CAIPM","COASP","CRAGE"],"Foundations":["CCT","CSCU","ECSS"]}
for t,c in tracks.items(): print(f"{t:24}: {', '.join(c)}")
PY
```

**Expected result:** the EC-Council **tracks** and credentials — the map this volume follows.

**Negative test:** assume EC-Council is only CEH; it spans **defense, forensics, SOC, cloud,
executive, and AI** — use the full track map.

**Cleanup:** none.

### Lab 1.2 — Understand the CEH exam model

**Objective:** Record the exam structure.

```python
python3 - <<'PY'
ceh={"Knowledge exam":"4 hours, 125 MCQ, ECC exam portal -> CEH",
     "Practical exam":"6 hours, 20 iLabs challenges -> combined = CEH Master",
     "Version":"v13 (AI-integrated)","Modules":20}
for k,v in ceh.items(): print(f"{k:16}: {v}")
PY
```

**Expected result:** the CEH **knowledge + practical** model and CEH Master — your scheduling
reference.

**Negative test:** expect one exam for CEH Master; it requires **both** the knowledge and practical
exams — plan for two.

**Cleanup:** none.

### Lab 1.3 — Plan an authorized, defensive path

**Objective:** Sequence credentials for a role.

```python
python3 - <<'PY'
paths={"Defender":"CND -> CSA -> ECIH","Authorized assessor":"CEH -> CEH Master -> CPENT",
       "Forensics/IR":"CHFI -> ECIH -> CTIA","Cloud/DevSecOps":"CCSE -> ECDE",
       "Leadership":"CEH -> CCISO"}
for role,path in paths.items(): print(f"{role:20}: {path}")
PY
```

**Expected result:** role-to-path sequences — the authorized, defensive ladder this volume follows.

**Negative test:** target CCISO with no security foundation; it expects **experience** — build the
track first.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

EC-Council certifies cybersecurity practitioners around the flagship CEH v13 (with AI) plus tracks
for pentest, network defense, forensics, SOC/IR/intel, cloud/DevSecOps/AppSec, executive, and AI —
ANSI-accredited and DoD 8140-aligned, taught here as authorized, defensive work.

- [ ] I can explain EC-Council's role and CEH v13.
- [ ] I can describe the CEH/CEH Master exam model.
- [ ] I can name the DoD-8140-aligned certs.
- [ ] I can plan an authorized, defensive path.
- [ ] I completed Labs 1.1–1.3 including each negative test.
