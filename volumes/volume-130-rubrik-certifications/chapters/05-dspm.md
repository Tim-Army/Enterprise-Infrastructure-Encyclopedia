# Chapter 05: Data Security Posture Management (DSPM)

## Learning Objectives

- Cover Rubrik's DSPM: discovering, classifying, and assessing the risk of sensitive data.
- Understand why knowing *what* data you have is the prerequisite to protecting it.
- Model sensitive-data classification and data-risk scoring.

## You can't protect what you can't see

**Data Security Posture Management (DSPM)** answers a question most organizations can't: *where is our sensitive data, who can access it, and how exposed is it?* Rubrik applies DSPM across the data it already sees (backups and live sources): discover sensitive data (PII, PHI, PCI, secrets), classify it, map who can access it, and score the risk — so security effort goes where the crown jewels actually are.

| DSPM step | What it produces |
|:---|:---|
| **Discovery** | Where sensitive data lives across the estate (often in surprising places) |
| **Classification** | What kind of sensitive data (PII/PHI/PCI/secrets) and how much |
| **Access analytics** | Who/what can reach it (over-permissioned access is the top risk) |
| **Risk scoring** | Prioritize by sensitivity × exposure × access breadth |

## Hands-On Lab

Python models classification and risk scoring. **Cost:** none.

### Lab 5.1 — Classify sensitive data

**Objective:** Discover and classify sensitive data across sources — the DSPM core.

```bash
python3 - <<'EOF'
import re
classifiers = {
  "PII (SSN)":    r"\b\d{3}-\d{2}-\d{4}\b",
  "PCI (card)":   r"\b(?:\d[ -]?){16}\b",
  "PHI (MRN)":    r"\bMRN[:# ]?\d{6,}\b",
  "Secret (key)": r"\bAKIA[0-9A-Z]{16}\b",
}
sources = {
  "finance/exports.csv": "SSN 123-45-6789 card 4111111111111111",
  "hr/notes.txt":        "employee MRN: 123456 medical",
  "devops/config.env":   "AWS AKIAIOSFODNN7EXAMPLE",
  "marketing/blog.md":   "no sensitive data here",
}
for path, content in sources.items():
    found = [name for name, pat in classifiers.items() if re.search(pat, content)]
    print(f"{path:<22} -> {', '.join(found) if found else 'no sensitive data'}")
EOF
```

**Expected result:** Each source classified — the finance CSV holds PII+PCI, HR notes hold PHI, a devops `.env` leaks a secret, marketing is clean. DSPM's discovery+classification finds sensitive data **wherever it actually is** (including a secret in a config file nobody thought to protect). You cannot prioritize protection without this map.

**Negative test:** Assuming sensitive data lives only in the "database" — the leaked AWS key in a config file and PHI in loose HR notes show it spreads everywhere; DSPM's estate-wide discovery is what catches the copies.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 5.2 — Score data risk (sensitivity × exposure × access)

**Objective:** Prioritize by risk, not by volume.

```bash
python3 - <<'EOF'
def data_risk(sensitivity, exposure, access_breadth):   # each 1..5
    score = sensitivity * exposure * access_breadth
    band = "LOW" if score <= 20 else "MEDIUM" if score <= 60 else "HIGH" if score <= 100 else "CRITICAL"
    return score, band
assets = [
  ("finance/exports.csv (PII+PCI, internet-exposed, all-staff read)", 5, 5, 5),
  ("hr/notes.txt (PHI, internal, HR-only)",                           4, 2, 1),
  ("devops/config.env (secret, in a repo, dev team)",                 5, 4, 3),
]
for name, s, e, a in assets:
    score, band = data_risk(s, e, a)
    print(f"[{band:8}] risk={score:3}  {name}")
EOF
```

**Expected result:**

```text
[CRITICAL] risk=125  finance/exports.csv (PII+PCI, internet-exposed, all-staff read)
[LOW     ] risk=  8  hr/notes.txt (PHI, internal, HR-only)
[HIGH    ] risk= 60  devops/config.env (secret, in a repo, dev team)
```

Risk = sensitivity × exposure × access breadth, so the internet-exposed, all-staff-readable PII+PCI file is CRITICAL while equally-sensitive but tightly-scoped PHI is LOW. DSPM directs effort by **risk**, not by data volume — the over-exposed crown jewels first. This access-breadth dimension (who can reach it) is often the dominant, most-fixable factor.

**Negative test:** Prioritizing by data *volume* (protect the biggest datasets first) — a huge low-sensitivity log matters less than a small internet-exposed PII file; risk scoring, not size, sets priority.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 5.3 — DSPM meets recovery

**Objective:** Connect DSPM to Rubrik's recovery side — the differentiator.

```bash
cat <<'EOF'
Why DSPM + backup together is powerful:
  - after a breach, DSPM tells you WHAT sensitive data was in the affected systems (breach scoping / notification)
  - it flags where sensitive data sprawled so you can reduce exposure BEFORE an incident
  - it prioritizes which workloads need the strongest SLA (Gold, immutable) — protect the crown jewels hardest
Rubrik's angle: the platform that already holds your data can also tell you what's sensitive and at risk.
EOF
```

**Expected result:** DSPM tied to recovery — after a breach it scopes *what sensitive data was exposed* (driving breach notification), and before one it reduces sprawl and informs SLA tiering (protect crown jewels with the strongest immutable policy). Rubrik's distinctive position is combining **what data you have** (DSPM) with **the ability to recover it** (backup) in one platform.

**Negative test:** Running DSPM and backup as disconnected tools — you know what's sensitive but can't easily act on it in recovery/notification; the integration is the value.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] Sensitive-data discovery and classification across sources drilled.
- [ ] Data-risk scoring (sensitivity × exposure × access breadth) internalized.
- [ ] DSPM-plus-recovery (breach scoping, sprawl reduction, SLA tiering) understood.
