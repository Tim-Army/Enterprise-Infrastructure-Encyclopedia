# Chapter 06: NCCSA — Data Loss Prevention

## Learning Objectives

- Cover the NCCSA's DLP pillar: detecting and controlling sensitive data in motion.
- Understand DLP rules, profiles, classification methods, and incident handling.
- Build DLP detection patterns with real regex.

## What DLP does

**Data Loss Prevention** finds sensitive data (PII, PCI, PHI, secrets, IP) in traffic and files and applies policy — block, alert, encrypt, or coach. In Netskope, DLP runs **inline** (on uploads/posts as they happen) and via **API** (on data already in sanctioned SaaS). The building blocks:

| Concept | Meaning |
|:---|:---|
| **DLP rule** | A detector: regex, keyword dictionary, data identifier (SSN, credit card), or fingerprint |
| **DLP profile** | A set of rules with thresholds, combined into a reusable detector |
| **Policy** | Ties a profile to a scope (app/activity/user) + an action (block/alert/coach/encrypt) |
| **Classification methods** | Regex/pattern, dictionaries, **Exact Data Match (EDM)**, fingerprinting, ML classifiers |
| **Incident** | A DLP match, surfaced for review/response in the console |

## Hands-On Lab

Real regex models the core detection. **Cost:** none.

### Lab 6.1 — Pattern-based detectors (regex)

**Objective:** Build detectors for common sensitive data.

```bash
python3 - <<'EOF'
import re
detectors = {
  "US SSN": r"\b\d{3}-\d{2}-\d{4}\b",
  "Credit Card (16-digit)": r"\b(?:\d[ -]*?){16}\b",
  "AWS Access Key": r"\bAKIA[0-9A-Z]{16}\b",
}
sample = "Contact 123-45-6789; card 4111 1111 1111 1111; key AKIAIOSFODNN7EXAMPLE ok"
for name, pat in detectors.items():
    hits = re.findall(pat, sample)
    print(f"{name:<24} matches={len(hits)} -> {'DETECTED' if hits else 'none'}")
EOF
```

**Expected result:**

```text
US SSN                   matches=1 -> DETECTED
Credit Card (16-digit)   matches=1 -> DETECTED
AWS Access Key           matches=1 -> DETECTED
```

Regex/data-identifier detectors are DLP's foundation — Netskope ships built-in identifiers for SSN, credit cards, and thousands of patterns; you also write custom regex. The NCCSA expects you to build and combine these into profiles.

**Negative test:** A credit-card regex with no validation (e.g. Luhn check) flags any 16 digits — false positives; production detectors add validators, and the exam tests knowing raw regex over-matches.

**Cleanup:** None.

### Lab 6.2 — Profiles with thresholds

**Objective:** Combine rules and set a match threshold to cut false positives.

```bash
python3 - <<'EOF'
import re
# a "PII profile": require MULTIPLE matches before firing (threshold), not a single stray number
ssn = re.compile(r"\b\d{3}-\d{2}-\d{4}\b")
def profile_hit(text, threshold=3):
    count = len(ssn.findall(text))
    return f"count={count} -> {'INCIDENT' if count >= threshold else 'below threshold (no action)'}"
print("one SSN:  ", profile_hit("ref 123-45-6789"))
print("bulk file:", profile_hit("\n".join(f"{i:03d}-45-6789" for i in range(50))))
EOF
```

**Expected result:**

```text
one SSN:   count=1 -> below threshold (no action)
bulk file: count=50 -> INCIDENT
```

Thresholds distinguish a stray reference from a **spreadsheet of records** — the difference between noise and a real breach. Profiles bundle detectors with match counts and proximity, the NCCSA's DLP-tuning skill.

**Negative test:** Threshold of 1 on a common pattern — every document with one number becomes an incident; alert fatigue buries real leaks. Thresholds are the tuning that makes DLP usable.

**Cleanup:** None.

### Lab 6.3 — Exact Data Match (EDM) concept

**Objective:** Understand precise detection of *your* specific records.

```bash
python3 - <<'EOF'
# EDM: match against a fingerprinted index of YOUR actual sensitive records (not patterns)
# e.g. your customer table's real SSNs/account numbers -> near-zero false positives
customer_ssns = {"123-45-6789", "987-65-4321"}   # (hashed/indexed in production)
def edm(value):
    return "EXACT MATCH (known customer record)" if value in customer_ssns else "not in EDM index"
print("123-45-6789 ->", edm("123-45-6789"))
print("111-11-1111 ->", edm("111-11-1111"))
EOF
```

**Expected result:**

```text
123-45-6789 -> EXACT MATCH (known customer record)
111-11-1111 -> not in EDM index
```

**Exact Data Match** compares against a fingerprinted index of your real records, so it flags *your* customers' data with almost no false positives — far more precise than pattern matching. NCCSA/NCCSI expect you to know EDM (and fingerprinting) for high-value structured/unstructured data.

**Negative test:** Using regex where EDM is needed — a regex for "SSN" flags every SSN-shaped string; EDM flags only *your* SSNs, the precision regulated data demands.

**Cleanup:** None.

### Lab 6.4 — Policy action and incident response

**Objective:** Tie a profile to an action and model incident handling.

```bash
python3 - <<'EOF'
# DLP policy: profile + scope + action; then the incident workflow
def dlp_policy(activity, profile_hit, destination):
    if profile_hit and destination == "personal-cloud": return "BLOCK + incident (high severity)"
    if profile_hit and activity == "external-share":     return "BLOCK + alert"
    if profile_hit:                                       return "ALERT + coach"
    return "ALLOW"
print("upload PII to personal cloud:", dlp_policy("upload", True, "personal-cloud"))
print("external share PII:          ", dlp_policy("external-share", True, "partner"))
print("internal move PII:           ", dlp_policy("move", True, "corp"))
EOF
```

**Expected result:** Graduated actions — block+high-severity incident for PII to a personal cloud, block+alert for external sharing, alert+coach internally — plus the incident that lands in the console for response. DLP is not just detection; it's the **action** and the **incident workflow** (assign, investigate, resolve), which the NCCSA covers.

**Negative test:** Detection with no action or no incident workflow — you log leaks but don't stop or investigate them; DLP's value is in the response, not the alert.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] Regex/data-identifier detectors built.
- [ ] Profiles with thresholds (noise vs real breach) tuned.
- [ ] Exact Data Match precision and the policy-action + incident workflow understood.
