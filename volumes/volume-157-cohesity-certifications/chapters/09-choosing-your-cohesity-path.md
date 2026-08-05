# Chapter 09: Choosing Your Cohesity Path

## Learning Objectives

- Sequence a Cohesity certification path by tier and role.
- Understand currency for a two-year-validity, evolving platform.
- Place Cohesity/data-security skills in the career.
- Assemble the volume into a study and career plan.

*Cert relevance: this chapter is the meta-guide — how to navigate the three-tier Academy program [Chapter 1](01-the-cohesity-program.md) laid out.*

## Sequencing your path

The Academy's three tiers ([Chapter 1](01-the-cohesity-program.md)) sequence naturally, and your path depends on **role** and **portfolio**:

| You are | Start | Then |
|:---|:---|:---|
| **Backup / data-protection admin** | Protection Associate — DataProtect ([COH100](03-dataprotect.md)) | Protection Professional |
| **Multicloud / cloud engineer** | Protection Associate — Multicloud | DataProtect Professional |
| **Files / storage engineer** | Implementation Professional — SmartFiles ([CCIP](05-smartfiles.md)) | DataProtect |
| **Security / SecOps** | Protection Associate — DataProtect | **Security Specialist** ([COH350](07-ai-powered-data-security.md)) |
| **NetBackup shop** | Protection Professional — NetBackup | NetBackup and Appliances |

**Protection Associate — DataProtect (COH100) is the natural entry point** — it validates the platform core the rest builds on. From there, climb to **Professional** (implement/operate) and, for security roles, the **Specialist** (the ransomware-resilience and AI-security depth). Cohesity recommends **~3 months of hands-on experience** before testing, so pair study with real platform time. The lab builds a sequence.

## Currency

Cohesity certifications are **valid for 2 years** ([Chapter 1](01-the-cohesity-program.md)), and the platform evolves quickly — **AI features** ([DataHawk/Gaia, Chapter 7](07-ai-powered-data-security.md)), cloud/multicloud capabilities, and the **integration of the Veritas/NetBackup portfolio** ([Chapter 8](08-netbackup-and-veritas.md)) are all moving. Treat the two-year cycle as a real refresh, and — because the [threat landscape shifts under every credential](../../volume-151-sentinelone-certifications/chapters/09-choosing-your-sentinelone-path.md) — keep current on ransomware techniques and recovery practice, not just product features. The lab covers currency.

## The data-security / resilience career

Cohesity skills sit in the **data-resilience and data-security** career — a field rising in importance precisely because **ransomware made data protection a board-level security concern.** A professional who understands immutable backup, cyber-vaulting, anomaly detection, and clean recovery is exactly who organizations need to answer "can we recover from ransomware?" — increasingly a survival question. The career pairs with the adjacent skills this shelf covers:

- **[Rubrik (CXXX)](../../volume-130-rubrik-certifications/README.md)** — the direct data-security peer; Cohesity vs Rubrik is *the* comparison.
- **[Commvault (CXXXIII)](../../volume-133-commvault-certifications/README.md)** — enterprise backup/recovery.
- **[CrowdStrike (L)](../../volume-050-crowdstrike-certifications/README.md) / [SentinelOne (CLI)](../../volume-151-sentinelone-certifications/README.md)** — endpoint threat detection; the prevention side of the ransomware fight (Cohesity is the recovery side).
- **Storage — [Everpure/Pure (CXXXVIII)](../../volume-138-everpure-purestorage-certifications/README.md)** — the primary storage backup protects.

Cohesity is the data-resilience specialty at the moment recovery became a security imperative. The lab positions it.

## Hands-On Lab

Python assembles a personal Cohesity plan. **Cost:** none.

### Lab 9.1 — Build your Cohesity path

**Objective:** Generate a tier- and role-appropriate sequence.

```bash
python3 - <<'EOF'
PATHS = {
  "backup / data-protection admin": [
    ("Protection Associate — DataProtect (COH100)", "the platform core (entry)"),
    ("Protection Professional", "implement + operate at scale"),
  ],
  "security / SecOps": [
    ("Protection Associate — DataProtect (COH100)", "know the platform"),
    ("Security Specialist (COH350)", "ransomware resilience + AI-security depth"),
  ],
  "NetBackup shop": [
    ("Protection Professional — NetBackup", "the Veritas enterprise backup line"),
    ("Protection Professional — NetBackup and Appliances", "+ the integrated appliances"),
  ],
}
role = "security / SecOps"   # change to taste
print(f"Cohesity Academy path for: {role}\n")
for i, (cert, why) in enumerate(PATHS[role], 1):
    print(f"   {i}. {cert:48} {why}")
print("\nGuidance:")
print("  - START with PROTECTION ASSOCIATE — DATAPROTECT (COH100): the platform core the")
print("    rest builds on. Climb to PROFESSIONAL (implement/operate), then SPECIALIST for")
print("    security roles (ransomware resilience + AI security).")
print("  - match certs to the PORTFOLIO you operate: Data Cloud, NetBackup (Veritas), or both.")
print("  - all PROCTORED, $200, valid 2 YEARS; ~3 months hands-on recommended — pair study")
print("    with real platform time.")
print("  - CURRENCY: the platform moves fast (AI/DataHawk/Gaia, multicloud, NetBackup")
print("    integration) + ransomware evolves — treat the 2-year cycle as a real refresh.")
EOF
```

**Expected result:** A role-based sequence anchored on Protection Associate — DataProtect (COH100), climbing to Professional and, for security roles, the Security Specialist. The build-your-path lesson is to start with the DataProtect associate (the platform core), match certifications to the portfolio you operate (Data Cloud, NetBackup, or both), pair study with hands-on time, and treat the two-year cycle as a real refresh as the platform and ransomware landscape evolve.

**Negative test:** Jumping to the Security Specialist without the platform foundation. The specialist depth assumes you know the Data Cloud; start with Protection Associate — DataProtect, then build to the security specialization.

**Cleanup:** None.

### Lab 9.2 — Position Cohesity in the data-security career

**Objective:** Map Cohesity/data-resilience skills to adjacent competencies.

```bash
python3 - <<'EOF'
ADJACENCIES = [
  ("Cohesity (data resilience)", "immutable backup + cyber-vault + AI detection", "the specialty itself"),
  ("Rubrik (CXXX)", "data security / backup",             "the direct peer (the comparison)"),
  ("Commvault (CXXXIII)", "enterprise backup/recovery",   "the enterprise peer"),
  ("CrowdStrike (L) / SentinelOne (CLI)", "endpoint threat detection", "PREVENT side (Cohesity = RECOVER side)"),
  ("Everpure / Pure (CXXXVIII)", "primary storage",       "what backup protects"),
]
print("Cohesity in the data-security / resilience skill map:\n")
print(f"   {'skill':38}{'domain':44}why it pairs")
for skill, domain, why in ADJACENCIES:
    print(f"   {skill:38}{domain:44}{why}")
print("\nThe career thesis: RANSOMWARE made data protection a BOARD-LEVEL security concern.")
print("A pro who gets immutable backup, cyber-vaulting, anomaly detection, and CLEAN")
print("recovery answers 'can we recover from ransomware?' — a survival question.")
print("\nThe rounded ransomware-defense picture:")
print("  PREVENT  (CrowdStrike/SentinelOne) — stop the attack at the endpoint")
print("  DETECT   (Cohesity DataHawk + EDR) — spot it early, in data + on endpoints")
print("  RECOVER  (Cohesity)                — the LAST line: immutable, vaulted, clean restore")
print("Prevention can fail; RECOVERY is what guarantees survival. Cohesity owns the")
print("resilience/recovery heart of it — pair it with Rubrik/Commvault (peers), EDR")
print("(prevention), and storage. Data resilience is a career, not just a backup admin job.")
EOF
```

**Expected result:** Cohesity mapped against Rubrik and Commvault (peers), CrowdStrike/SentinelOne (endpoint prevention), and Pure (storage), showing the prevent/detect/recover picture. The career-positioning lesson closes the volume: ransomware made data protection a board-level security concern, and Cohesity owns the resilience/recovery heart of it — the last line that guarantees survival when prevention fails — pairing with the backup peers, endpoint prevention, and storage skills the rest of the shelf teaches.

**Negative test:** Treating backup as separate from security. Since ransomware, recovery *is* a security function — the last line of defense — and Cohesity skills belong alongside endpoint prevention and detection in an integrated ransomware-defense strategy.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] A Cohesity path sequenced by tier and role, anchored on Protection Associate — DataProtect (COH100).
- [ ] Currency understood — the two-year cycle as a real refresh on a fast-moving AI/multicloud/NetBackup platform.
- [ ] Cohesity positioned in the data-security/resilience career alongside Rubrik, Commvault, EDR, and storage.
- [ ] The volume assembled into a personal study and career plan — prevent, detect, recover.
