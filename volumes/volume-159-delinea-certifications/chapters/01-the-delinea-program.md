# Chapter 01: The Delinea Security Academy Certification Program

![The Delinea Security Academy certification program and the PAM platform beneath it. Delinea is a Privileged Access Management leader formed from the 2021 merger of Thycotic and Centrify. The Security Academy certification program has three tiers. Associate is a self-paced, online-only certification of e-learning coursework and an online exam, for partners and customers building deep technical understanding toward the Engineer tier. Engineer empowers customers and partners to install, configure, and manage to best practice, validated through hands-on lab challenges assessed by a live Delinea Security Academy expert, including break-fix troubleshooting. Consultant, by invitation only, adds customizations, integrations, and extensibility through self-paced coursework, an online exam, and hands-on technical labs. Certified professionals receive a printable certificate and digital badges, and can request Not-for-Resale license keys for hands-on practice. The platform beneath spans Secret Server for credential vaulting and session recording, Privilege Manager for endpoint least privilege, Server PAM for server privilege and Active Directory bridging, DevOps Secrets Vault, Account Lifecycle Manager, and the unified Delinea Platform extending into identity threat detection.](../../../diagrams/volume-159-delinea-certifications/chapter-01-program.svg)

*Figure 1-1. The three Security Academy tiers and the Delinea PAM platform they validate.*

## Learning Objectives

- Describe the Delinea Security Academy program — Associate, Engineer, Consultant tiers.
- Distinguish the e-learning exam from the expert-assessed hands-on labs.
- Place the Delinea product portfolio and its Thycotic/Centrify heritage.
- Recognize Delinea's position as a PAM leader alongside BeyondTrust and CyberArk.

> **Defensive framing.** This volume is about *defending* privileged access — vaulting credentials, enforcing least privilege on endpoints and servers, governing service accounts, and detecting identity threats. PAM is a defensive control discipline. Nothing here is about attacking systems.

## What Delinea is

Delinea is a leader in **Privileged Access Management (PAM)** — securing, controlling, and monitoring **privileged access** (administrator, root, and service accounts), the highest-leverage defensive control since privileged-credential abuse runs through nearly every breach. Delinea was formed from the **2021 merger of Thycotic and Centrify**, combining Thycotic's **Secret Server** vault and **Privilege Manager** with Centrify's **server PAM** and Active Directory bridging into one portfolio, now unified as the **Delinea Platform**.

Delinea is one of the three PAM leaders this shelf covers, alongside [BeyondTrust (CLVI)](../../volume-156-beyondtrust-certifications/README.md) and [CyberArk (LXXVII)](../../volume-077-cyberark-certifications/README.md) — the **PAM trio**, and understanding one sharpens the others.

## The program

Delinea's **Security Academy** runs the certification program across **three tiers**, awarding **digital badges** and printable certificates. Free training is delivered through **Delinea University**:

| Tier | For | Format |
|:---|:---|:---|
| **Associate** | Customers/partners building technical understanding toward Engineer | Self-paced, online-only: **e-learning + an online exam** |
| **Engineer** | Customers/partners who install, configure, and manage to best practice | **Hands-on lab challenges assessed by a live Delinea expert** (incl. break-fix) |
| **Consultant** | Partners doing customizations, integrations, extensibility | Coursework + online exam + hands-on labs — **by invitation only** |

The tiers rise from **knowledge** (Associate) through **hands-on capability** (Engineer) to **advanced extensibility** (Consultant). The lab models the program.

## The expert-assessed Engineer tier

The **Engineer** tier is worth dwelling on: rather than a multiple-choice exam alone, it validates capability through **hands-on lab challenges assessed by a live Delinea Security Academy expert** — you install and configure real use cases and **troubleshoot break-fix scenarios**, and a human expert judges whether you did it correctly. This is a **prove-you-can-do-it** model (like the practical exams the [OffSec volume (XLIII)](../../volume-043-offensive-security-certifications/README.md) uses, but for defensive PAM operations), and it makes the Engineer credential a strong signal of real operational skill, not just recall. **NFR (Not-for-Resale) license keys** are available by request so candidates can practice hands-on. The lab models the assessment model.

## The product portfolio

Every credential sits on the Delinea portfolio:

| Product | Secures | Heritage |
|:---|:---|:---|
| **Secret Server** | Credential vaulting, rotation, session recording ([Ch 3](03-secret-server.md)) | Thycotic |
| **Privilege Manager** | Endpoint least privilege ([Ch 4](04-privilege-manager.md)) | Thycotic |
| **Server PAM** | Server privilege, AD bridging ([Ch 5](05-server-pam.md)) | Centrify |
| **DevOps Secrets Vault** | Secrets for DevOps/machines ([Ch 6](06-devops-secrets-and-machine-identity.md)) | Delinea |
| **Account Lifecycle Manager** | Service-account governance ([Ch 7](07-account-lifecycle-manager.md)) | Delinea |
| **Delinea Platform + ITDR** | Unified SaaS + identity security ([Ch 8](08-the-delinea-platform-and-identity-security.md)) | Delinea |

The next chapter frames Delinea and the PAM landscape; the middle chapters take each product; Chapter 9 sequences a path. The lab maps the portfolio.

## Hands-On Lab

Python models the program. **Cost:** none.

### Lab 1.1 — Map the Security Academy tiers

**Objective:** Represent the three tiers and their assessment models.

```bash
python3 - <<'EOF'
TIERS = {
  "Associate":  {"for": "build technical understanding (toward Engineer)",
                 "assess": "e-learning coursework + online exam", "access": "self-paced, online-only"},
  "Engineer":   {"for": "install/configure/manage to best practice",
                 "assess": "hands-on LAB CHALLENGES assessed by a LIVE expert (+ break-fix)", "access": "hands-on labs"},
  "Consultant": {"for": "customizations/integrations/extensibility",
                 "assess": "coursework + online exam + hands-on labs", "access": "BY INVITATION ONLY"},
}
print("Delinea Security Academy — three certification tiers:\n")
for i, (tier, d) in enumerate(TIERS.items(), 1):
    print(f"   {i}. {tier}")
    print(f"      for:    {d['for']}")
    print(f"      assess: {d['assess']}")
    print(f"      access: {d['access']}\n")
print("The arc: ASSOCIATE (knowledge, e-learning + exam) -> ENGINEER (hands-on capability,")
print("★ labs graded by a LIVE expert incl. break-fix) -> CONSULTANT (extensibility, invite-only).")
print("Rewards: printable certificate + DIGITAL BADGES; free training via Delinea University;")
print("NFR (Not-for-Resale) license keys by request to practice hands-on.")
print("Delinea = Thycotic (Secret Server, Privilege Manager) + Centrify (Server PAM) merged 2021,")
print("now unified as the Delinea Platform. A PAM leader with BeyondTrust (CLVI) + CyberArk (LXXVII).")
EOF
```

**Expected result:** The three Security Academy tiers — Associate (e-learning + online exam), Engineer (expert-assessed hands-on labs including break-fix), and invitation-only Consultant — with digital badges and NFR practice keys. The program lesson is that Delinea rises from knowledge to hands-on capability to extensibility, validating the Engineer tier through live-expert-graded labs, over a portfolio formed from the 2021 Thycotic + Centrify merger.

**Negative test:** Assuming the Engineer tier is a multiple-choice exam. It is validated through hands-on lab challenges a live Delinea expert assesses (including break-fix troubleshooting) — a prove-you-can-do-it model, not recall.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 1.2 — Why an expert-assessed practical tier

**Objective:** Contrast recall testing with hands-on expert assessment.

```bash
python3 - <<'EOF'
# two ways to validate a PAM engineer; score what each actually proves
MODELS = {
  "multiple-choice only": {"proves_knowledge": True, "proves_can_configure": False, "proves_can_troubleshoot": False},
  "expert-assessed labs":  {"proves_knowledge": True, "proves_can_configure": True,  "proves_can_troubleshoot": True},
}
print("What does each assessment model actually prove?\n")
for model, p in MODELS.items():
    score = sum(p.values())
    print(f"   {model:24} knowledge={p['proves_knowledge']}  configure={p['proves_can_configure']}  troubleshoot={p['proves_can_troubleshoot']}  -> proves {score}/3")
print("\nDelinea's ENGINEER tier uses EXPERT-ASSESSED LABS: a live Delinea Security Academy")
print("expert watches you install/configure real use cases AND fix break-fix scenarios.")
print("This proves you can actually OPERATE the platform (configure + troubleshoot), not just")
print("that you recognize the right answer. For a PAM system — where a misconfiguration can")
print("expose the crown-jewel credentials — proving hands-on competence matters. It's the")
print("defensive-operations counterpart to a practical pentest exam: demonstrate, don't recite.")
EOF
```

**Expected result:** A multiple-choice model proving only knowledge (1/3) versus expert-assessed labs proving knowledge, configuration, and troubleshooting (3/3). The lesson is that Delinea's Engineer tier validates real operational competence — configuring use cases and fixing break-fix scenarios under a live expert's assessment — which matters for a PAM system where a misconfiguration can expose the crown-jewel credentials.

**Negative test:** Judging PAM competence by a knowledge quiz alone. Operating a vault, session recording, and least-privilege policies is a hands-on skill; only a practical, assessed lab proves the candidate can configure and troubleshoot it.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] The program understood — Delinea Security Academy, Associate/Engineer/Consultant tiers, digital badges.
- [ ] The expert-assessed Engineer tier understood — hands-on labs and break-fix judged by a live expert.
- [ ] The product portfolio placed, and the 2021 Thycotic + Centrify heritage understood.
- [ ] Delinea recognized as a PAM leader alongside BeyondTrust (CLVI) and CyberArk (LXXVII).
