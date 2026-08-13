# Chapter 07: AI-Powered Data Security

## Learning Objectives

- Explain how Cohesity applies AI to data security (DataHawk).
- Describe threat detection, classification, and clean-recovery identification.
- Understand Gaia — generative-AI search over your data.
- Recognize AI as a differentiator across the data-security platform.

*Cert relevance: AI-powered security is a Cohesity differentiator and central to the Security Specialist (COH350).*

## AI applied to data security

Cohesity's positioning as **"AI-powered data security and management"** is not just branding — it applies **AI** to the security problems backup data creates and solves. The core product is **DataHawk**, Cohesity's data-security service, which uses AI/ML for **threat detection**, **data classification**, and **cyber-vaulting** integration. The premise is that Cohesity **sees all your data** (every backup, all your files), which is exactly the corpus AI needs to find threats, locate sensitive data, and identify clean recovery points. Backup is a uniquely rich vantage point, and AI turns that visibility into security insight. The lab models AI-driven detection.

## Threat detection, classification, and clean recovery

DataHawk's AI serves several security functions:

- **Threat detection** — ML models spot **ransomware behavior** in backup data ([the anomaly patterns of Chapter 4](04-ransomware-resilience.md)) — mass changes, encryption entropy, unusual access — and can scan for known **threat indicators (IOCs)** and malware in backups, so you don't restore infected data.
- **Data classification** — AI **scans and classifies** the data across the estate, identifying **sensitive data** (PII, PHI, financial, secrets) so you know what you hold and can govern it — critical for compliance (GDPR, HIPAA) and for understanding blast radius after a breach.
- **Clean-recovery identification** — combining detection across snapshots to pinpoint the **last clean copy** before an attack, so recovery restores uninfected data.

AI makes the backup platform actively *intelligent* about threats and sensitive data, not just a passive store. The lab models classification and detection.

## Gaia: generative-AI search

**Gaia** is Cohesity's **generative-AI** capability — a **conversational search** interface that lets you **ask questions of your own data** in natural language and get answers, drawing on the backup corpus. Because Cohesity holds a vast, indexed copy of enterprise data, generative AI can turn it into a **knowledge base** you can query — "where is our customer PII?", "which documents mention this contract?" — safely, over data you already have, without exposing it to external services. Gaia represents the shift from backup-as-insurance to backup-as-**an active, queryable data asset**, with AI unlocking value from data that otherwise just sits in cold storage. The lab models AI search.

## AI as a platform differentiator

AI runs across the platform — detection ([resilience, Chapter 4](04-ransomware-resilience.md)), classification and governance (files, [Chapter 5](05-smartfiles.md)), and search (Gaia) — making it a genuine **differentiator** in the [data-protection market versus peers like Rubrik (CXXX)](../../volume-130-rubrik-certifications/README.md) and [Commvault (CXXXIII)](../../volume-133-commvault-certifications/README.md), who are all racing to add AI. For a certification candidate, understanding *how* AI applies to data security — detection, classification, clean recovery, and search — is increasingly central, as reflected in the Security Specialist track. The lab synthesizes.

## Hands-On Lab

Python models AI-driven data security. **Cost:** none.

### Lab 7.1 — AI detection, classification, and clean-recovery selection

**Objective:** See AI turn backup visibility into security insight.

```bash
python3 - <<'EOF'
# DataHawk-style AI over the backup corpus: detect threats, classify sensitive data, pick clean copy
snapshots = [
    {"day": 1, "anomaly": False, "malware_ioc": False},
    {"day": 2, "anomaly": False, "malware_ioc": False},
    {"day": 3, "anomaly": False, "malware_ioc": False},
    {"day": 4, "anomaly": True,  "malware_ioc": True},   # attack
]
files = [
    {"path": "/hr/ssns.csv",        "class": "PII (SSN)"},
    {"path": "/fin/cardholder.xlsx","class": "PCI (card data)"},
    {"path": "/eng/readme.md",      "class": "non-sensitive"},
    {"path": "/health/records.db",  "class": "PHI"},
]
print("AI-POWERED DATA SECURITY (DataHawk-style) over the backup corpus:\n")
print("1) THREAT DETECTION — scan snapshots for anomalies + malware IOCs:")
clean = None
for s in snapshots:
    bad = s["anomaly"] or s["malware_ioc"]
    if not bad: clean = s["day"]
    print(f"     day {s['day']}: {'THREAT (anomaly/IOC)' if bad else 'clean'}")
print(f"   -> last CLEAN recovery point: day {clean} (restore this, not the infected copy)\n")
print("2) DATA CLASSIFICATION — AI scans + labels sensitive data across the estate:")
sensitive = 0
for f in files:
    flag = "  <-- SENSITIVE (govern/protect)" if f["class"]!="non-sensitive" else ""
    if flag: sensitive += 1
    print(f"     {f['path']:22} {f['class']}{flag}")
print(f"   -> {sensitive}/{len(files)} sensitive -> know what you hold (GDPR/HIPAA/PCI + breach blast radius)\n")
print("3) GAIA (generative AI) — ask your data in natural language:")
print('     Q: "where is our customer PII?"  -> A: /hr/ssns.csv, /health/records.db ...')
print("\nCohesity SEES ALL your data (every backup, all files) — the exact corpus AI needs.")
print("It turns that visibility into SECURITY: detect ransomware + malware (don't restore")
print("infected data), CLASSIFY sensitive data (govern + know breach blast radius), pick the")
print("CLEAN recovery point, and QUERY your data conversationally (Gaia). Backup becomes an")
print("active, intelligent, queryable asset — AI is the differentiator vs Rubrik/Commvault.")
EOF
```

**Expected result:** AI scanning snapshots to flag the day-4 threat and select day 3 as the clean recovery point, classifying the PII/PCI/PHI files as sensitive, and answering a natural-language query via Gaia. The AI lesson is that Cohesity's total data visibility is the corpus AI needs to detect threats, avoid restoring infected data, classify sensitive data for governance and breach blast-radius, and make backup a queryable asset — the platform differentiator.

**Negative test:** Treating backup as a passive store with no analysis. You would restore infected data, not know where sensitive data lives, and leave the corpus's value untapped; AI-driven detection, classification, and search turn visibility into security insight.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] AI-powered data security understood — DataHawk applying AI/ML to the backup corpus.
- [ ] Threat detection, data classification, and clean-recovery identification understood.
- [ ] Gaia understood — generative-AI conversational search over your own data.
- [ ] AI recognized as a platform differentiator across detection, governance, and search.
