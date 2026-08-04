# Chapter 65: Appendix — Practical Offensive/Defensive Certifications (HTB, TCM, INE) and Course Access

The **practical, hands-on** security certification providers — **Hack The Box (HTB Academy)**, **TCM
Security**, and **INE Security** (formerly eLearnSecurity) — their certifications, training, and access
model. Verified on **4 August 2026** from **academy.hackthebox.com/certifications**,
**certifications.tcm-sec.com**, and **ine.com / security.ine.com**, the sources that anchor [Volume
CXXXI — Practical Offensive and Defensive Certification Tracks](../../volume-131-practical-offensive-certifications/README.md).
Third-party exam-dump sites were excluded as sources.

> **Authorization frame.** These are certifications for **authorized, in-scope** penetration testing and
> security analysis. Everything here — and in Volume CXXXI — is for understanding attacks well enough to
> **detect, prevent, respond to, and report** them, practiced only against systems you own or have signed
> permission to test (your own lab, a provider's sanctioned exam range, or a scoped engagement). The
> volume's labs model **methodology and defensive lessons** in free Python; they are not operational
> attack tooling.

**How access works.** All three share a **prove-it-by-doing** model: you are certified by completing a
**real exam lab** (a network, web app, Active Directory domain, or SOC scenario) and writing a
**professional report**, not by answering multiple-choice questions.

- **HTB Academy** — subscription/module study (job-role paths); each certification exam requires a
  **voucher**; exams are hands-on labs with a report. Many free modules; the certifications are paid.
- **TCM Security** — affordable, **non-proctored**, ~12-month course access, **free exam retake**,
  cloud-hosted exam labs; **learning-path bundles** and discounts (military/veterans/students/teachers/
  first responders).
- **INE Security** — subscription training (INE Premium) **plus** exam vouchers, or standalone; **free
  retake**; a certification voucher is included with some subscription tiers. eLearnSecurity heritage.

## Free and low-cost resources and entry points

- **[HTB Academy](https://academy.hackthebox.com/)** and **[Hack The Box Labs](https://www.hackthebox.com/)** — free modules, free/practice machines, then paid certifications
- **[TCM Security Academy](https://academy.tcm-sec.com/)** — low-cost courses; several free/intro courses; certifications at [certifications.tcm-sec.com](https://certifications.tcm-sec.com/)
- **[INE / security.ine.com](https://ine.com/)** — training subscription; **eJPT** is a popular free-to-low-cost entry point
- **Sanctioned practice only:** each provider's own exam range or your **own isolated lab VMs** — never a system you do not own or are not authorized to test
- **Free study lab:** any Linux host with `python3` models the volume's defensive methodology — attack-path graphs to defend, detection rules, IR timelines, secure-coding fixes, and report structure

## Fees, delivery, and renewal

- **Fees:** HTB certifications are voucher-priced (roughly **$490** for associate/specialist tiers,
  **$1260** for expert tiers — confirm current pricing); TCM and INE price per certification/bundle,
  both with **free retakes**. Lab practice on free primitives is free.
- **Delivery:** self-paced online study; **hands-on exam labs** with a required professional **report**
  (windows range from ~8 hours to ~5 days depending on the certification).
- **Prerequisites:** none formal; the associate/junior certifications (CJCA, PJPT, eJPT) are the
  designed entry points.
- **Validity/renewal:** these programs move fast and add certifications frequently (the AI ones are
  recent). Some tie certifications to versioned material; verify each provider's current recertification
  policy before planning.

## The certifications

Verified 4 August 2026. **O** = offensive (understood to defend), **B** = blue-team/defensive, **AI** =
AI/LLM security.

### Hack The Box (HTB Academy)

| Credential | Focus | Type |
| --- | --- | --- |
| CJCA — Certified Junior Cybersecurity Associate | Hybrid offensive+defensive foundation | O/B |
| CPTS — Certified Penetration Testing Specialist | Intermediate network pentest + commercial report | O |
| CWES — Certified Web Exploitation Specialist | Web pentest / bug bounty | O |
| CWEE — Certified Web Exploitation Expert | Advanced web (black/white box), secure coding | O |
| CAPE — Certified Active Directory Pentesting Expert | AD/Windows: Kerberos/NTLM, ADCS/WSUS/Exchange/trusts, C2 | O |
| CWPE — Certified Wi-Fi Pentesting Expert | WPA2/WPA3/WPA-Enterprise | O |
| CDSA — Certified Defensive Security Analyst | SOC operations, incident handling, detection | B |
| COAE — Certified Offensive AI Expert | AI red team; co-developed with Google; aligns SAIF + OWASP LLM/ML/Agentic Top 10 | AI |

### TCM Security

| Credential | Focus | Type |
| --- | --- | --- |
| PJPT — Practical Junior Penetration Tester | Internal AD attack path (2-day + report) | O |
| PNPT — Practical Network Penetration Tester | External + internal engagement (5-day + report) — **flagship** | O |
| PWPA / PWPP / PWPE — Practical Web Pentest Associate/Professional/Expert | Web application security ladder | O |
| PORP — Practical OSINT Research Professional | OSINT / reconnaissance (3-day) | O |
| PMRP — Practical Malware Research Professional | Malware analysis (5-day) | O |
| PIPA — Practical IoT Pentest Associate | IoT/hardware | O |
| PMPA — Practical Mobile Pentest Associate | Mobile application security | O |
| PAPA — Practical AI Pentest Associate | Agentic AI security | AI |
| PHDA — Practical Help Desk Associate | Help-desk/IT foundation (8-hour) | B |
| PSAA / PSAP — Practical SOC Analyst Associate/Professional | SOC analysis (2-day / 3-day) | B |

### INE Security (eLearnSecurity)

| Credential | Focus | Type |
| --- | --- | --- |
| eJPT — Junior Penetration Tester | Famous entry-level practical cert | O |
| eCPPT — Certified Professional Penetration Tester | Hand-graded professional pentest | O |
| eWPT / eWPTX — Web Application Pentester / eXtreme | Web application security (advanced eXtreme) | O |
| eMAPT — Mobile Application Penetration Tester | Mobile application security | O |
| eAIS — AI Systems Security Specialist | AI/LLM attack and defensive controls | AI |
| eSOC — SOC Analyst | SOC Tier-1 operations | B |
| eIAMA — Identity & Access Management Technologist | Zero-trust / IAM | B |
| eEDA — Enterprise Defense Administrator | Enterprise defense | B |
| eCIR — Certified Incident Responder | Incident response | B |
| eCTHP — Certified Threat Hunting Professional | Proactive threat hunting | B |
| eCDFP — Certified Digital Forensics Professional | Digital forensics | B |

## Notes

- **The unifying trait is practical assessment:** a real exam lab plus a professional report, mirroring a
  real engagement — the model employers value because it maps to job capability.
- **Red *and* blue with the same rigor:** distinctively in this batch, all three providers certify
  **defensive/blue-team** work (CDSA; PSAA/PSAP/PHDA; eSOC/eCIR/eCTHP/eEDA/eIAMA/eCDFP) alongside
  offensive — the offensive knowledge exists to power the defense.
- **The AI wave:** COAE (with Google), PAPA, and eAIS are recent additions reflecting how quickly AI
  systems became attack targets; the OWASP LLM Top 10 is a defender's checklist.
- **Peers in the encyclopedia:** [OffSec XLIII](../../volume-043-offensive-security-certifications/README.md)
  (OSCP+), [GIAC LXXIV](../../volume-074-giac-certifications/README.md) (SANS),
  [EC-Council LXXV](../../volume-075-ec-council-certifications/README.md) (CEH), and the governance
  programs [ISC2 XL](../../volume-040-isc2-certifications/README.md) and
  [CompTIA XXXIX](../../volume-039-comptia-certification-tracks/README.md).
- **Authorization is the profession's foundation:** the same skill set is a respected career or a crime;
  the only difference is signed, in-scope permission.
