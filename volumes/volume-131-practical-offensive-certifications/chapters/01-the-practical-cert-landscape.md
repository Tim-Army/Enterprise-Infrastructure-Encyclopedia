# Chapter 01: The Practical Certification Landscape (HTB, TCM, INE)

![The practical, hands-on offensive-and-defensive security certification landscape across three providers: Hack The Box (HTB CJCA/CPTS/CWES/CDSA/CWEE/CAPE/CWPE/COAE), TCM Security (PJPT/PNPT/web PWPA-PWPP-PWPE/PORP/PMRP/PIPA/PAPA/PMPA and defensive PHDA/PSAA/PSAP), and INE Security (eJPT/eCPPT/eWPT/eWPTX/eMAPT/eAIS and defensive eSOC/eIAMA/eEDA/eCIR/eCTHP/eCDFP). All are exam-lab-based — you prove skills by doing in a real environment and writing a professional report — and all are for authorized, ethical, in-scope work only.](../../../diagrams/volume-131-practical-offensive-certifications/chapter-01-certification-program.svg)

*Figure 1-1. Three providers of practical, hands-on certifications — assessed by doing, not by multiple choice — spanning offensive testing and the defensive analysis that answers it. Every technique in this volume is for authorized, in-scope, educational work only.*

## Learning Objectives

- Describe the practical-certification landscape across Hack The Box, TCM Security, and INE Security.
- Understand what "practical, hands-on, exam-lab-based" means and why it differs from multiple-choice exams.
- Internalize the ethical and legal frame that governs everything in this volume: authorization first.
- Set up a free study environment for the defensive-methodology labs.

## Authorization first — the non-negotiable frame

This volume covers certifications that teach **penetration testing and security analysis**. Every offensive technique exists here for one purpose: **to understand attacks well enough to detect, prevent, and respond to them**, and only ever practiced against systems you are **explicitly authorized** to test — your own lab, a provider's sanctioned exam range, or an engagement with a signed scope. Testing systems you do not own or have written permission to test is illegal.

Accordingly, this volume's labs model **methodology and defensive lessons** — how an attack path works so you can break it, how to structure a report, how to write a detection — using free primitives. They do not provide operational tooling to attack real targets. The certifications themselves are respected industry credentials for defenders and authorized testers alike.

## What "practical" means

These providers share a defining trait: you are certified by **doing the work in a real environment**, then **writing a professional report** — not by answering multiple-choice questions. That is the volume's thesis:

| Exam style | What it proves |
|:---|:---|
| Multiple-choice | Recall and recognition |
| **Practical / hands-on lab** | You can actually perform the task, under time pressure, and communicate it |

A practical exam gives you a live lab (a network, a web app, an AD domain, a SOC scenario), a time window (hours to days), and requires a **report** — mirroring a real engagement. Employers value this because it maps directly to job capability.

## The three providers

Verified on the providers' sites, 4 August 2026:

| Provider | Model | Flagship / notable |
|:---|:---|:---|
| **Hack The Box (HTB Academy)** | Module-based training + exam-lab vouchers, tied to job-role paths | **CPTS** (pentest), **CDSA** (defensive), **CAPE** (AD), **COAE** (Offensive AI, co-developed with Google) |
| **TCM Security** | Affordable, non-proctored cloud exam labs; 12-mo training access; free retake | **PNPT** (network pentest, 5-day + report), **PJPT** (AD), defensive **PSAA/PSAP** (SOC) |
| **INE Security** (formerly eLearnSecurity) | Subscription + voucher (free voucher with Premium); hand-graded | **eJPT** (famous entry), **eCPPT**, **eWPTX**, defensive **eSOC/eCIR/eCTHP/eCDFP** |

All three span **offensive** (recon, network/AD, web, mobile, IoT, AI) and **defensive/blue-team** (SOC, incident response, threat hunting, forensics) tracks — reflecting that the same knowledge serves attack and defense. Newer additions across all three cover **AI/LLM security** (HTB COAE, TCM PAPA, INE eAIS).

## Hands-On Lab

The labs model defensive methodology with **free Python/Linux** — no offensive tooling against real targets. **Cost:** none.

### Lab 1.1 — Map the landscape and the authorization boundary

**Objective:** Fix the provider structure and the ethical frame.

```bash
cat <<'EOF'
Practical (hands-on exam lab + report) providers:
  HTB:  CJCA · CPTS · CWES · CDSA · CWEE · CAPE · CWPE · COAE (job-role paths)
  TCM:  PJPT · PNPT · PWPA/PWPP/PWPE · PORP · PMRP · PIPA · PAPA · PMPA | PHDA/PSAA/PSAP (blue)
  INE:  eJPT · eCPPT · eWPT · eWPTX · eMAPT · eAIS | eSOC/eIAMA/eEDA/eCIR/eCTHP/eCDFP (blue)
AUTHORIZATION RULE: only ever test systems you own or have SIGNED, IN-SCOPE permission to test.
Everything offensive here is to understand attacks so you can DEFEND — in an authorized lab only.
EOF
```

**Expected result:** The three catalogs and the authorization rule — the boundary that governs the entire volume. The structure organizes the chapters: reconnaissance ([02](02-reconnaissance-and-osint.md)), methodology/reporting ([03](03-methodology-and-reporting.md)), network/AD defended ([04](04-network-and-active-directory.md)), web ([05](05-web-application-security.md)), and the blue-team side ([06](06-blue-team-soc-detection.md)–[07](07-incident-response-hunting-forensics.md)), plus AI security ([08](08-ai-llm-security.md)).

**Negative test:** Practicing any technique against a system you don't own or have written authorization for — illegal, regardless of intent; the sanctioned lab/exam range is the only place to build these skills.

**Cleanup:** None.

### Lab 1.2 — Stand up the study lab

**Objective:** Prepare the free primitives for the defensive-methodology labs.

```bash
python3 -c "import re, json, hashlib, datetime; print('stdlib available for methodology/detection/report modeling')"
echo "lab ready: python models attack-path graphs (to defend), detection rules, IR timelines, report structure"
echo "for hands-on offensive practice, use ONLY the providers' sanctioned exam ranges or your own isolated lab VMs"
```

**Expected result:** Python present — this volume models the *methodology, defensive lessons, detection, and reporting* on one host. For actual offensive practice, the providers' own sanctioned ranges (or your isolated lab) are the authorized environment; never a third-party system.

**Negative test:** Treating this volume's models as attack tools — they are defensive/educational models; the authorization boundary from Lab 1.1 always applies.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] The three providers (HTB/TCM/INE) and their practical, exam-lab model understood.
- [ ] The practical-vs-multiple-choice distinction and its job-capability value internalized.
- [ ] The authorization-first ethical/legal frame accepted as non-negotiable.
- [ ] The free study lab stood up for the defensive-methodology labs.
