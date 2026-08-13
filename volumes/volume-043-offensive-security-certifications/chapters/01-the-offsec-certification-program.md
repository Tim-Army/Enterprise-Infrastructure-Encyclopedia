# Chapter 01: The OffSec Certification Program

## Learning Objectives

- Explain what OffSec certifies and why its exams are hands-on and proctored.
- Describe the credential map across penetration testing, web, exploit development, defense, and AI security.
- Explain the course-code system, the exam-plus-report format, and the OSCE³ expert designation.
- Describe the "+" renewal model and which credentials expire.
- Understand the authorization and ethics that govern all offensive practice in this volume.

## Theory and Architecture

**OffSec** (Offensive Security) publishes the industry's best-known **hands-on**
security certifications — most famously the **OSCP**. What sets them apart is
that the exams are **practical and proctored**: candidates spend many hours
compromising or defending machines in a controlled lab, then write a professional
**report**. There are no multiple-choice domains to memorize; the credential
proves you can *do the work*. That places this volume alongside the encyclopedia's
hands-on security volumes (Cybersecurity X, and the CompTIA PenTest+/Ethical
Hacker material in XXXIX) at the practitioner tier.

The program maps to **courses** (a course code earns a certification) across
disciplines:

- **Foundational** — **OSCC** (CyberCore: SEC-100, and SJD-100) and **KLCP**
  (Kali Linux Certified Professional, PEN-103).
- **Penetration Testing** — **OSCP/OSCP+** (PEN-200), **OSEP** (PEN-300), **OSWP**
  (PEN-210).
- **Web Security** — **OSWA** (WEB-200), **OSWE** (WEB-300).
- **Exploit Development** — **OSED** (EXP-301), **OSEE** (EXP-401).
- **Defensive Security** — **OSDA** (SOC-200), **OSIR** (IR-200), **OSTH**
  (TH-200).
- **AI Security** — **OSAI** (AI-300, the OffSec AI Red Teamer).

Earning the three core 300-level credentials — **OSEP + OSWE + OSED** — grants
**OSCE³**, OffSec's expert-tier umbrella. **OSEE** is the top exploit-development
credential.

## Design Considerations

Plan an OffSec path by **role and depth**, and expect a steep, hands-on climb
(the culture's motto is "Try Harder"). A newcomer starts **Foundational** (OSCC,
KLCP), then most take the flagship **OSCP+** (PEN-200) as the pivot into
professional penetration testing. From there, specialize: **advanced pentest**
(OSEP, OSWP), **web** (OSWA → OSWE), **exploit development** (OSED → OSEE),
**defense** (OSDA, OSIR, OSTH), or **AI red teaming** (OSAI). Because the exams
are performance-based, prepare by **living in a lab** — OffSec's own lab
environments and your own vulnerable VMs — not by reading.

Note the **renewal model**. OffSec introduced a **"+" model**: **OSCP+**, the
**OSCC** variants, **OSTH**, **OSIR**, and **OSAI+** are valid **three years**
and renewed via OffSec's CPE program, a recertification exam, or another
qualifying exam. Classic credentials — **OSEP, OSWE, OSED, OSEE**, and the
lifetime **OSCP** — do **not** expire.

## Implementation and Automation

Every skill in this volume is practiced against **authorized targets only** — the
OffSec lab, an intentionally vulnerable VM you own (for example, a local
Metasploitable or a deliberately weak container), or a CTF you are entitled to
play. The labs here focus on **methodology and enumeration** with standard tools,
run against **your own machine or lab**:

```bash
# Confirm the practitioner's toolkit (Kali or equivalent) is present
for t in nmap gobuster hydra sqlmap john hashcat; do command -v "$t" >/dev/null \
  && echo "$t: ok" || echo "$t: install from your distro/Kali"; done
```

## Validation and Troubleshooting

Confirm a credential's course, exam format, and status on the OffSec course page:

```text
offsec.com/courses > open the course:
  - the certification it earns and the course code (e.g., PEN-200 -> OSCP/OSCP+)
  - the exam format (practical hours + report) and passing score
  - prerequisites and recommended prior courses
  - whether it uses the "+" three-year renewal or does not expire
```

Common pitfalls: expecting a **multiple-choice** exam (OffSec exams are
**practical**); assuming **OSCP** and **OSCP+** are the same (OSCP is lifetime,
OSCP+ is the three-year renewable version earned from the same PEN-200 exam); and
practicing techniques **outside an authorized lab** — that is illegal and against
the OffSec code of conduct.

## Security and Best Practices

**Authorization is the first control.** Never run offensive tooling against a
system you do not own or have explicit written permission to test — this volume's
labs target your own machine or an authorized lab, and every technique is taught
to be understood and **defended against**. Use official OffSec courses and lab
time, document everything (the **report** is half the exam skill), and follow the
**OffSec code of conduct** and the law. For blue-team credentials (OSDA/OSIR/OSTH),
the same offensive knowledge is applied to **detection and response**.

## References and Knowledge Checks

- offsec.com: the course-and-certification catalog; per-course exam guides; the OffSec code of conduct.

**Knowledge checks**

1. Why are OffSec exams practical rather than multiple-choice?
2. Which three credentials earn OSCE³, and which credentials never expire?
3. What is the single most important precondition before any offensive practice?

## Hands-On Lab

Exam-preparation walkthroughs for reading the program and preparing an authorized
lab. **All commands target your own machine only.**

**Shared prerequisites for Labs 1.1–1.3** — a Kali (or equivalent) shell with
`nmap`; a local, authorized lab VM or `localhost`. **Cost:** none.

### Lab 1.1 — Enumerate the certification catalog (Topic: Read the program)

**Objective:** List the current courses and the credentials they earn.

```bash
curl -sSL "https://www.offsec.com/courses/" \
  | grep -oiE '(PEN|WEB|EXP|SOC|IR|TH|SEC|AI|SJD)-[0-9]{3}' | sort -u | head -20
```

**Expected result:** the current course codes (`PEN-200`, `PEN-300`, `WEB-200`,
`WEB-300`, `EXP-301`, `SOC-200`, `IR-200`, `TH-200`, `SEC-100`, `AI-300`, …) —
the whole program in one view.

**Negative test:** rely on an old list; it will miss the **AI-300 (OSAI)** and
**CyberCore (OSCC)** additions and the OSCP → OSCP+ change — use the live catalog.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 1.2 — Verify your authorized lab (Topic: Authorization first)

**Objective:** Confirm you are only targeting a system you own.

```bash
ip -brief addr | awk '{print $1, $3}'      # your own host's addresses
echo "Scope rule: only these addresses (or an OffSec lab you are enrolled in) are in scope."
```

**Expected result:** your host's own addresses — the *only* legitimate target
outside an enrolled OffSec lab. Authorization defines scope before any tool runs.

**Negative test:** point a scanner at an address you do not own "just to test";
that is unauthorized access — never scan outside your own systems or an
authorized lab.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 1.3 — A first enumeration pass on localhost (Topic: Methodology)

**Objective:** Run the enumeration step every OffSec course begins with — on your
own host.

```bash
nmap -sT -p- --min-rate 1000 127.0.0.1 | grep -E 'open|Nmap done'
```

**Expected result:** a list of open TCP ports on your **own** loopback interface
(or none) — the enumeration-first methodology that underpins every OffSec
credential.

**Negative test:** skip enumeration and jump to exploitation; OffSec's method is
**enumerate thoroughly first** — most footholds come from careful enumeration.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

OffSec certifies hands-on security skill through practical, proctored exams plus a
professional report, across penetration testing, web, exploit development,
defense, and the new AI red-teaming track. Courses map to credentials by code;
OSCE³ is earned from OSEP + OSWE + OSED; and a "+" model gives some credentials a
renewable three-year life while others never expire. Every technique is practiced
only against authorized targets and taught to be defended against.

- [ ] I can map OffSec's disciplines and their course codes.
- [ ] I can explain the practical exam-plus-report format and OSCE³.
- [ ] I can distinguish OSCP from OSCP+ and the "+" renewal model.
- [ ] I understand that authorization is the precondition for all practice.
- [ ] I completed Labs 1.1–1.3 including each negative test.
