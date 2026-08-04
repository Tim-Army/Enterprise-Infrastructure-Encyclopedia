# Chapter 01: The Commvault Program and Readiverse Academy

![The Commvault certification program in Readiverse Academy, structured as four tiers on one path: Commvault Cloud Practitioner (foundational platform and cyber resilience, earned via the Commvault Cloud Administrator course, the Cyber Resilience course, one workload course, and exams for the Administrator and Cyber Resilience components), Commvault Cloud Specialist (expanded operational, workload, and security depth), Commvault Cloud Professional (advanced recovery and workload expertise including Cloud Rewind or Cleanroom Recovery coursework), and Commvault Cloud Expert (cloud engineering and resilience leadership). All four rest on three learning pillars — foundational platform skills, cyber resilience, and workload and feature expertise — and are earned through a combination of coursework, hands-on lab activities, and validated assessments. Commvault is an ISC2 CPE Authorized Submitter, so coursework also earns continuing-education credits toward ISC2 certifications.](../../../diagrams/volume-133-commvault-certifications/chapter-01-certification-program.svg)

*Figure 1-1. Readiverse Academy's four tiers and three learning pillars, with the named certifications that populate them.*

## Learning Objectives

- Describe the Readiverse Academy four-tier certification structure.
- Identify the three learning pillars and the named certifications.
- Explain how Commvault positions data protection as a cyber-resilience discipline.
- Set up a free study environment for the data-protection labs.

## What Commvault does

Commvault is a **data protection and cyber resilience** vendor. The product line — **Commvault Cloud**, available as SaaS, as software you run, and as hybrid deployments — protects data across data centers, clouds, and SaaS applications, and increasingly frames that protection as a **security** control rather than an operations chore.

That framing is the thing to understand before the certifications make sense. A backup platform in 2026 is judged on whether it can survive and recover from a **ransomware attack**: whether copies are immutable, whether infection can be detected in the backup data, and whether a clean recovery can be rehearsed and proven. Commvault's newer capabilities — **Threat Scan**, **Cleanroom Recovery**, **Cloud Rewind** — all address that question, and they appear directly in the certification tiers.

## Readiverse Academy: four tiers, one path

Commvault's training and certification program runs in **Readiverse Academy**, whose tagline for the credential program is "**four tiers, one path**" and, pointedly, "vendor-validated credentials, not just course completions." Certifications are earned through a **combination of coursework, hands-on lab activities, and validated assessments** — not by watching videos alone.

The tier structure was introduced in **June 2026**, so it is new; expect it to keep evolving.

| Tier | Focus |
|:---|:---|
| **Commvault Cloud Practitioner** | Foundational platform and cyber-resilience knowledge |
| **Commvault Cloud Specialist** | Expanded operational, workload, and security depth |
| **Commvault Cloud Professional** | Advanced recovery and workload expertise, including **Cloud Rewind** or **Cleanroom Recovery** coursework |
| **Commvault Cloud Expert** | Cloud engineering and resilience leadership: **Cloud Engineer** coursework, advanced features, Cloud Rewind, and Cleanroom Recovery |

The **Practitioner** tier's requirements were published in detail and show the pattern for the rest:

- **Commvault Cloud Administrator** course (~4 hours)
- **Cyber Resilience** course (~4 hours)
- **One workload course** (~30 minutes)
- **Exams** for the Administrator and Cyber Resilience components
- Claim the **digital badge**

Note what that composition says: even the entry tier requires platform skills *and* cyber resilience *and* a workload — the three pillars, from the beginning.

## The three learning pillars

Every tier is built on the same three skill areas, and they map to this volume's chapters:

| Pillar | What it covers | Chapters |
|:---|:---|:---|
| **Foundational platform skills** | Architecture, storage, policies, deduplication, backup/recovery operations | [02](02-commvault-cloud-architecture.md)–[05](05-backup-and-recovery-operations.md) |
| **Cyber resilience** | Immutability, air gap, anomaly detection, Threat Scan, clean recovery | [06](06-cyber-resilience-immutability-threat-scan.md)–[07](07-cleanroom-recovery-and-cloud-rewind.md) |
| **Workload and feature expertise** | Microsoft 365, Active Directory/Entra ID, VMware, Oracle, file servers | [08](08-workload-protection.md) |

## The named certifications

Readiverse lists individual certifications that populate the tiers:

| Certification | Subject |
|:---|:---|
| **Commvault Cloud Administrator** | The platform administration core |
| **Cyber Resilience Certification** | The resilience/security half |
| **Commvault Cloud SaaS — Threat Scan** | Detecting threats and corruption in protected data |
| **Commvault Cloud SaaS — Cleanroom Recovery** | Isolated, clean recovery environments |
| **Commvault Cloud SaaS — Cloud Rewind** | Cloud application rebuild and recovery |

Alongside these sit **workload courses** ("Workload Hero") for Microsoft 365, Active Directory and Entra ID, file servers, VMware, and Oracle; short "Problem Solvers" courses for specific tasks; and live simulation events — the **Cyber Resilience Workshop** (2 hours), **Minutes to Meltdown** (a ransomware simulation), and **Minutes to Recovery** (a 3-hour exercise in which participants take the attacker, defender, and recovery roles in turn).

## ISC2 CPE credit

**Commvault is an ISC2 CPE Authorized Submitter.** Readiverse coursework can earn **continuing professional education credits** toward ISC2 certifications such as the CISSP ([Volume XL](../../volume-040-isc2-certifications/README.md)). If you hold an ISC2 credential and need CPEs anyway, this training pays twice — a genuinely useful piece of program design worth knowing about.

## Free study environment

Commvault Cloud is commercial software, so this volume's labs model the **data-protection disciplines** — retention and tiering, deduplication, RPO/RTO, immutability and WORM, anomaly detection, cleanroom orchestration, workload protection matrices — in free Python. The concepts are what the exams test and what transfer across platforms.

## Hands-On Lab

### Lab 1.1 — Set up the study environment

**Objective:** Confirm the free toolchain for the volume.

```bash
python3 --version
mkdir -p ~/commvault-study && cd ~/commvault-study
python3 - <<'EOF'
print("Data protection study environment ready.")
print("Labs model: retention/tiering, deduplication, RPO/RTO, immutability,")
print("anomaly detection, cleanroom recovery, workload matrices — no Commvault license needed.")
EOF
```

**Expected result:** Python reports a version and the message prints. Every lab uses only the standard library — the protection logic, not the vendor console, is the transferable skill.

**Negative test:** Assuming you need a licensed CommCell to learn data protection — retention math, deduplication ratios, RPO/RTO arithmetic, and immutability semantics are all vendor-independent and can be reasoned about locally.

**Cleanup:** `rm -rf ~/commvault-study` when done.

### Lab 1.2 — Map the tiers to a study plan

**Objective:** Choose your tier and see what each requires.

```bash
python3 - <<'EOF'
tiers = {
  "Practitioner": {"focus":"foundational platform + cyber resilience",
                   "requires":["Cloud Administrator course (4h)","Cyber Resilience course (4h)",
                               "one workload course (~30m)","exams: Administrator + Cyber Resilience","claim badge"]},
  "Specialist":   {"focus":"expanded operational, workload, security depth","requires":["builds on Practitioner"]},
  "Professional": {"focus":"advanced recovery + workload expertise","requires":["Cloud Rewind or Cleanroom Recovery coursework"]},
  "Expert":       {"focus":"cloud engineering + resilience leadership",
                   "requires":["Cloud Engineer coursework","advanced feature courses","Cloud Rewind","Cleanroom Recovery"]},
}
for name, t in tiers.items():
    print(f"\nCommvault Cloud {name} — {t['focus']}")
    for r in t["requires"]:
        print(f"   - {r}")
print("\nAll four rest on the same three pillars: platform skills, cyber resilience, workload expertise.")
print("Bonus: Readiverse coursework earns ISC2 CPEs (Commvault is an Authorized Submitter).")
EOF
```

**Expected result:** The four tiers print with their requirements, showing the ladder from Practitioner to Expert. The important structural insight is that resilience is not a bolt-on at the top — the Practitioner tier already requires a Cyber Resilience course and exam, because Commvault treats backup as a security control from the first tier.

**Negative test:** Studying only platform administration and skipping the resilience material — you cannot complete even the Practitioner tier, which requires both exams.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] The four Readiverse tiers named and their focus described.
- [ ] The three learning pillars identified and mapped to chapters.
- [ ] The named certifications (Administrator, Cyber Resilience, Threat Scan, Cleanroom, Cloud Rewind) listed.
- [ ] The ISC2 CPE benefit understood.
- [ ] Free Python study environment ready.
