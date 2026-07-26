# Chapter 03: Security, Compliance, and Identity Certifications

## Learning Objectives

- Enumerate the current SC-family certifications and their exam codes.
- Distinguish the identity, operations, information-security, and architect roles.
- Recognize the SC renames and additions — SC-401 and the new SC-500.
- Map each credential to hands-on skills across Volumes XXXVII and X.
- Build a security-focused study path from Fundamentals to Expert.

## Theory and Architecture

The **Security, Compliance, and Identity (SC)** family certifies the security
roles across Microsoft 365, Entra ID, Azure, and Microsoft Purview and
Defender. As verified on Microsoft Learn (26 July 2026), the current
credentials are:

- **Microsoft Certified: Security, Compliance, and Identity Fundamentals** —
  exam **SC-900** (Fundamentals). Zero Trust concepts and the Microsoft
  identity, security, compliance, and Defender/Purview landscape.
- **Microsoft Certified: Identity and Access Administrator Associate** — exam
  **SC-300** (Associate). Entra ID identities, authentication, Conditional
  Access, and identity governance.
- **Microsoft Certified: Security Operations Analyst Associate** — exam
  **SC-200** (Associate). Threat detection and response with Microsoft
  Defender XDR and Sentinel.
- **Microsoft Certified: Information Security Administrator Associate** — exam
  **SC-401** (Associate). Information protection, DLP, and compliance with
  Microsoft Purview. **SC-401 replaced the retired SC-400** (Information
  Protection Administrator).
- **Microsoft Certified: Cybersecurity Architect Expert** — exam **SC-100**
  (Expert). Design a Zero Trust security strategy and architecture across
  identity, data, applications, and infrastructure.
- **Microsoft Certified: Cloud and AI Security Engineer Associate** — exam
  **SC-500** (Associate). A newer credential covering securing cloud and AI
  workloads — one of the post-2025 additions to the family.

## Design Considerations

The SC family has clear role lanes. **SC-300** is for **identity and access**
engineers; **SC-200** for the **SOC/threat** analyst; **SC-401** for
**information protection and compliance**; **SC-100** for the **security
architect**; and the new **SC-500** for **cloud and AI security**
engineering — a signal of how much AI-workload security now matters.

Sequence deliberately: **SC-900 → (SC-300 and/or SC-200 and/or SC-401) →
SC-100**. SC-100 is Expert and cross-domain, and Microsoft recommends real
experience with at least one Associate area first. Pair SC credentials with
the hands-on identity and security work in **Volume XXXVII** (Conditional
Access, Purview, Defender XDR — Chapters 03, 10, 11) and the broader security
foundations in **Volume X — Enterprise Cybersecurity**.

## Implementation and Automation

Verify the SC family and the renames from Microsoft Learn:

```bash
for slug in security-compliance-and-identity-fundamentals identity-and-access-administrator \
            security-operations-analyst information-security-administrator \
            cybersecurity-architect-expert cloud-and-ai-security-engineer-associate; do
  code=$(curl -s "https://learn.microsoft.com/en-us/credentials/certifications/$slug/" \
    | grep -oE '\bSC-[0-9]{3}\b' | sort -u | tr '\n' ' ')
  echo "$slug -> $code"
done
# information-security-administrator -> SC-401  (replaced SC-400)
# cloud-and-ai-security-engineer-associate -> SC-500  (new)
```

## Validation and Troubleshooting

Map credentials to blueprints and practice:

| Credential | Exam | Tier | Practice in |
| --- | --- | --- | --- |
| SC Fundamentals | SC-900 | Fundamentals | Vol X Ch 01; Vol XXXVII Ch 03 |
| Identity and Access Administrator | SC-300 | Associate | Vol XXXVII Ch 02–04 |
| Security Operations Analyst | SC-200 | Associate | Vol XXXVII Ch 11; Vol X |
| Information Security Administrator | SC-401 | Associate | Vol XXXVII Ch 10 |
| Cybersecurity Architect Expert | SC-100 | Expert | Vol X; Vol XXXVII |
| Cloud and AI Security Engineer | SC-500 | Associate | Vol XXXVII Ch 11; Vol XXXIII |

Common pitfalls: studying **SC-400** (retired — the current information-
security exam is **SC-401**); missing the new **SC-500** in an older program
map; and taking **SC-100** without Associate-level experience — as an Expert
architecture exam it assumes fluency across identity, data, and infrastructure
security.

## Security and Best Practices

Prepare with **Microsoft Learn** paths and **free practice assessments**, and
get hands-on with Conditional Access, Purview, and Defender in a developer
tenant (Volume XXXVII). Verify **SC-401** and **SC-500** on Learn — both are
recent changes an older study guide will get wrong. Because the SC family
overlaps Microsoft 365 and Azure security, plan it alongside **MS-102** and
the Azure security content (Volume XXXIII). Renew annually through the free
assessment.

## References and Knowledge Checks

- Microsoft Learn: certification pages for SC-900, SC-300, SC-200, SC-401, SC-100, SC-500.
- Cross-reference: [Volume XXXVII](../volume-37-microsoft-365-modern-work/README.md), [Volume X — Enterprise Cybersecurity](../volume-10-enterprise-cybersecurity/README.md).

**Knowledge checks**

1. Which exam replaced SC-400, and what does it cover?
2. What role does the new SC-500 certify?
3. Why sequence SC-100 after an Associate credential?

## Hands-On Lab

Exam-preparation walkthroughs for the SC family.

**Shared prerequisites for Labs 3.1–3.2** — a browser; `curl` for Lab 3.1.
**Cost:** none.

### Lab 3.1 — Confirm the SC renames (Topic: Verify currency)

**Objective:** Prove SC-401 and SC-500 from Learn.

```bash
curl -s "https://learn.microsoft.com/en-us/credentials/certifications/information-security-administrator/" | grep -oE '\bSC-[0-9]{3}\b' | sort -u
curl -s "https://learn.microsoft.com/en-us/credentials/certifications/cloud-and-ai-security-engineer-associate/" | grep -oE '\bSC-[0-9]{3}\b' | sort -u
```

**Expected result:** **SC-401** and **SC-500** respectively — the current
information-security exam and the new cloud-and-AI-security exam.

**Negative test:** look for SC-400 on the information-security page; it is not
there — SC-400 retired.

**Cleanup:** none.

### Lab 3.2 — Build a security path (Topic: Study plan)

**Objective:** Sequence the SC family for a SOC-plus-identity role.

```text
SC-900 (Fundamentals)
  -> SC-300 (Identity and Access) + SC-200 (Security Operations)
  -> SC-401 (Information Security) as compliance depth
  -> SC-100 (Cybersecurity Architect Expert) once cross-domain experience exists.
Practice: Vol XXXVII Ch 03 (Conditional Access), Ch 10 (Purview), Ch 11 (Defender XDR).
```

**Expected result:** a Fundamentals→Associate→Expert security path anchored to
hands-on labs.

**Negative test:** target SC-100 first; the architect exam's breadth is very
hard without the Associate foundation.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The SC family runs SC-900 (Fundamentals), SC-300 (Identity and Access),
SC-200 (Security Operations), SC-401 (Information Security, replacing SC-400),
SC-100 (Cybersecurity Architect Expert), and the new SC-500 (Cloud and AI
Security Engineer). The credentials map to Conditional Access, Purview, and
Defender practice in Volume XXXVII and the security foundations in Volume X.

- [ ] I can list the SC credentials and exam codes.
- [ ] I know SC-401 replaced SC-400 and SC-500 is new.
- [ ] I can map each to hands-on practice.
- [ ] I can sequence a security study path to Expert.
- [ ] I completed Labs 3.1–3.2 including each negative test.
