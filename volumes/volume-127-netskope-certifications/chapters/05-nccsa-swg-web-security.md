# Chapter 05: NCCSA — Secure Web Gateway and Threat Protection

## Learning Objectives

- Cover the NCCSA's SWG pillar: web filtering, SSL inspection, and threat protection.
- Understand URL categorization, SSL decryption trade-offs, and inline malware defense.
- Model URL filtering and SSL-inspection decisions with free primitives.

## What the SWG does

A **Secure Web Gateway** inspects and controls internet-bound web traffic: block malicious/inappropriate sites, enforce acceptable use, inspect encrypted traffic, and stop malware inline. In a SASE model the SWG runs at the **edge** (NewEdge), so remote users get the same protection as those in the office, without backhaul.

| Function | What it does |
|:---|:---|
| **URL filtering** | Allow/block/coach by category (malware, phishing, gambling, etc.) and custom lists |
| **SSL/TLS inspection** | Decrypt to inspect encrypted traffic (where policy and privacy allow) |
| **Threat protection** | Anti-malware, sandboxing, C2/callback detection on web downloads |
| **Content control** | File-type controls, safe search, tenant restrictions |

## Hands-On Lab

nftables/squid and Python model filtering and inspection decisions. **Cost:** none.

### Lab 5.1 — URL categorization and filtering

**Objective:** Model category-based allow/block/coach.

```bash
python3 - <<'EOF'
# URL filtering by category with an action per category
categories = {"malware":"BLOCK", "phishing":"BLOCK", "gambling":"BLOCK",
              "social-media":"COACH", "news":"ALLOW", "business":"ALLOW"}
def classify(url):
    if "casino" in url: return "gambling"
    if "login-verify" in url: return "phishing"
    if "facebook" in url or "twitter" in url: return "social-media"
    return "business"
for url in ["casino-x.com","login-verify-bank.tld","facebook.com","erp.corp.com"]:
    cat = classify(url); print(f"{url:<24} [{cat:<12}] -> {categories.get(cat,'ALLOW')}")
EOF
```

**Expected result:**

```text
casino-x.com             [gambling    ] -> BLOCK
login-verify-bank.tld    [phishing    ] -> BLOCK
facebook.com             [social-media] -> COACH
erp.corp.com             [business    ] -> ALLOW
```

Category-based filtering with per-category actions — including **coach** (warn the user and let them proceed with justification), a middle ground between allow and block that the NCCSA emphasizes. Custom URL lists override categories.

**Negative test:** Block-only policy for social media when the marketing team needs it — you generate tickets; **coaching** balances risk and productivity, which the exam highlights.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 5.2 — SSL/TLS inspection decisions

**Objective:** Model where to decrypt and where not to.

```bash
python3 - <<'EOF'
# SSL inspection: decrypt to inspect, but respect privacy/compliance bypasses
def inspect(url, category):
    sensitive = {"health","finance-banking","government"}
    if category in sensitive:
        return "BYPASS decryption (privacy/compliance)"
    return "DECRYPT + inspect (threat/DLP visibility)"
for url, cat in [("mybank.com","finance-banking"),("random-download.io","file-share"),("clinic.example","health")]:
    print(f"{url:<22} [{cat:<16}] -> {inspect(url,cat)}")
EOF
```

**Expected result:**

```text
mybank.com             [finance-banking ] -> BYPASS decryption (privacy/compliance)
random-download.io     [file-share      ] -> DECRYPT + inspect (threat/DLP visibility)
clinic.example         [health          ] -> BYPASS decryption (privacy/compliance)
```

SSL inspection is what makes threat and DLP visibility possible (most traffic is encrypted), but banking/health/government categories are commonly **bypassed** for privacy/compliance. Balancing coverage against privacy is a core NCCSA SWG skill.

**Negative test:** Decrypt everything including banking/health — a compliance and trust problem (and some apps pin certificates and break); selective bypass is mandatory, not optional.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 5.3 — Certificate-pinning and bypass reality

**Objective:** Understand why some traffic can't be decrypted.

```bash
cat <<'EOF'
Why SSL inspection needs bypass lists:
  - certificate pinning: some apps (update agents, some mobile apps) reject the inspection cert -> break
  - privacy/compliance: health, finance, government categories
  - the Netskope root CA must be trusted on endpoints for decryption to work at all
Bypass the un-decryptable/sensitive; inspect the rest. Steering (Ch03) + inspection scope define coverage.
EOF
```

**Expected result:** The operational reality — pinned apps and sensitive categories go on bypass lists, and endpoints must trust the Netskope CA for decryption to work. NCCSA troubleshooting often traces "app broken after enabling SSL inspection" to pinning.

**Negative test:** Enabling SSL inspection without deploying the CA to endpoints — every HTTPS site throws certificate errors; the CA distribution is a prerequisite the exam checks.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 5.4 — Inline threat protection

**Objective:** Model malware defense on a web download.

```bash
python3 - <<'EOF'
# Inline threat protection: hash/signature + sandbox verdict on a download
known_bad = {"e3b0c442"}   # (toy hash) known-malicious
def scan(file_hash, sandbox_verdict):
    if file_hash in known_bad: return "BLOCK (known malware signature)"
    if sandbox_verdict == "malicious": return "BLOCK (sandbox detonation)"
    return "ALLOW"
print("known-bad download:", scan("e3b0c442","unknown"))
print("zero-day download: ", scan("abcd1234","malicious"))
print("clean download:    ", scan("beef9999","benign"))
EOF
```

**Expected result:**

```text
known-bad download: BLOCK (known malware signature)
zero-day download:  BLOCK (sandbox detonation)
clean download:     ALLOW
```

Inline threat protection combines signatures (known malware) with **sandboxing** (detonate unknowns to catch zero-days) on web downloads — done at the edge, inline, so it stops the file before it lands. This is the SWG's threat half the NCCSA tests.

**Negative test:** Signature-only protection misses zero-days; the sandbox is what catches novel malware, and the exam expects you to know inline threat protection combines both.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] URL categorization with allow/block/coach modeled.
- [ ] SSL-inspection scope (decrypt vs privacy/pinning bypass) and CA prerequisite understood.
- [ ] Inline threat protection (signatures + sandbox) drilled.
