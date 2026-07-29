# Chapter 06: Certified Cloud Security Professional (CCSP)

## Learning Objectives

- Explain what CCSP certifies and its relationship to CISSP and the Cloud Security Alliance.
- List the six CCSP domains and their exam weights.
- Describe the CCSP exam mechanics and the 1 August 2026 outline refresh.
- Apply cloud-security thinking: shared responsibility, data security, and cloud IAM.
- Complete a per-domain walkthrough for each CCSP domain.

## Theory and Architecture

The **Certified Cloud Security Professional (CCSP)** is the specialist credential
for securing cloud environments — architecture, data, platform, applications,
operations, and the legal and compliance overlay. It was **co-created by ISC2
and the Cloud Security Alliance (CSA)** and maps to the CSA's guidance and the
**shared-responsibility model**. It requires **five years** of experience (with
substitutions: a CISSP counts for the full requirement, a CCSK for one domain).

The exam is **125 items in 3 hours**, pass mark **700/1000**. The current outline
weights the domains:

| # | Domain | Weight |
|---|--------|--------|
| 1 | Cloud Concepts, Architecture and Design | 17% |
| 2 | Cloud Data Security | 20% |
| 3 | Cloud Platform and Infrastructure Security | 17% |
| 4 | Cloud Application Security | 17% |
| 5 | Cloud Security Operations | 16% |
| 6 | Legal, Risk and Compliance | 13% |

**Cloud Data Security (20%)** is the heaviest domain — the data lifecycle,
encryption, and key management dominate cloud-security practice.

> **Currency note:** ISC2 has announced a **new CCSP exam outline effective 1
> August 2026**. Confirm the domains and weights on the official CCSP exam
> outline before scheduling on or after that date.

## Design Considerations

CCSP complements the encyclopedia's **cloud volumes** (AWS XVII, Azure XXXIII,
Google Cloud XXXIV) at the governance-and-architecture level: those teach a
provider's security *services*; CCSP teaches the vendor-neutral **principles**
that decide when and how to use them. The **shared-responsibility model** is the
organizing idea — what the provider secures (the cloud) versus what the customer
secures (in the cloud) shifts across IaaS, PaaS, and SaaS, and CCSP tests the
boundary constantly. Prioritize **Domain 2 (data)** and treat **key management**
(who holds the keys — provider, BYOK, or HYOK) as the crux of cloud data
security.

## Implementation and Automation

CCSP concepts are provider-agnostic, so the labs below use portable tools —
`openssl` for the encryption and key concepts at the heart of Domain 2, and
illustrative cloud-CLI patterns (as used elsewhere in the encyclopedia) for
data-security, IAM, and logging controls. The reasoning transfers to any
provider's console.

## Validation and Troubleshooting

Confirm the CCSP blueprint before studying:

```text
isc2.org > Certifications > CCSP > Exam Outline:
  - six domains and weights (17/20/17/17/16/13 currently)
  - 125 items, 3 hours, 700/1000
  - five years experience (CISSP substitutes fully; CCSK for one domain)
  - new outline effective 1 August 2026
```

Common pitfalls: memorizing one provider's service names instead of the
**vendor-neutral concept**; misplacing the **shared-responsibility boundary**
across service models; and underestimating **key management** — encryption is
only as strong as key custody.

## Security and Best Practices

Default to **customer-controlled encryption keys** for sensitive data, enforce
least privilege in **cloud IAM**, log control-plane and data-plane activity, and
treat the **shared-responsibility model** as a written agreement, not an
assumption. Maintain CCSP with CPE and AMF; it is DoD 8140-recognized for cloud
roles.

## References and Knowledge Checks

- isc2.org: *CCSP* page and Exam Outline; *CCSP Official Study Guide*; Cloud Security Alliance guidance.

**Knowledge checks**

1. Which CCSP domain is heaviest, and why?
2. How does the shared-responsibility boundary move across IaaS, PaaS, and SaaS?
3. What is the difference between BYOK and HYOK key management?

## Hands-On Lab

Per-topic walkthroughs — **one lab for every weighted CCSP domain**. Cloud-CLI
commands are illustrative patterns; no cloud account is required to study them.

**Shared prerequisites** — a Linux shell with `python3` and `openssl`.
**Cost:** none.

### Lab 6.1 — CCSP: Cloud Concepts, Architecture and Design (17%)

**Objective:** Map the shared-responsibility boundary across service models.

```bash
python3 - <<'PY'
layers = ["data","application","runtime","OS","virtualization","hardware"]
resp = {"IaaS":3, "PaaS":2, "SaaS":1}   # customer secures top N layers
for model,n in resp.items():
    cust=", ".join(layers[:n]); prov=", ".join(layers[n:])
    print(f"{model}: customer -> {cust:35} | provider -> {prov}")
PY
```

**Expected result:** the customer's responsibility shrinks from IaaS to SaaS
while the provider's grows — the shared-responsibility model CCSP centers on.

**Negative test:** assume "the cloud provider secures everything"; the customer
always owns at least the data and access — misplacing the boundary causes
breaches.

**Cleanup:** none.

### Lab 6.2 — CCSP: Cloud Data Security (20%)

**Objective:** Encrypt data client-side so the provider stores only ciphertext
(the BYOK/HYOK principle).

```bash
head -c 32 /dev/urandom | base64 > dek.key            # customer-held data key
echo "PII: 123-45-6789" > record.txt
openssl enc -aes-256-cbc -pbkdf2 -in record.txt -out record.enc -pass file:dek.key
echo "Upload record.enc; the provider never sees plaintext or the key."
```

**Expected result:** `record.enc` is ciphertext encrypted under a
**customer-held** key — the data-security control (client-side encryption /
key custody) that dominates Domain 2.

**Negative test:** rely only on provider-side encryption with provider-managed
keys for the most sensitive data; the provider (and a subpoena) can access it —
hold your own keys when the threat model requires.

**Cleanup:** `rm -f dek.key record.txt record.enc`

### Lab 6.3 — CCSP: Cloud Platform and Infrastructure Security (17%)

**Objective:** Express least-privilege network security-group rules as data.

```bash
python3 - <<'PY'
sg = [("web","0.0.0.0/0","tcp/443","allow"),
      ("app","sg-web","tcp/8443","allow"),
      ("db","sg-app","tcp/5432","allow"),
      ("db","0.0.0.0/0","tcp/5432","DENY (never expose DB publicly)")]
for tier,src,port,act in sg: print(f"{tier:4} from {src:10} {port:9} -> {act}")
PY
```

**Expected result:** tiered security-group rules where the database accepts only
the app tier and never the internet — cloud infrastructure segmentation.

**Negative test:** open the database port to `0.0.0.0/0` "temporarily"; public
database exposure is a top cloud breach cause — never do it.

**Cleanup:** none.

### Lab 6.4 — CCSP: Cloud Application Security (17%)

**Objective:** Validate a JWT's signature-verification requirement (cloud API
auth).

```bash
python3 - <<'PY'
# A JWT has header.payload.signature; the API MUST verify the signature + claims
parts = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJhcHAifQ.SIGNATURE".split(".")
print(f"segments: {len(parts)} (header, payload, signature)")
print("Verify: signature (key), exp/nbf (time), iss/aud (issuer/audience) BEFORE trusting claims.")
PY
```

**Expected result:** a 3-segment token and the verification checklist — the
token-validation discipline of cloud application security (Domain 4).

**Negative test:** decode a JWT and trust its claims without verifying the
signature; anyone can forge unsigned claims — always verify first.

**Cleanup:** none.

### Lab 6.5 — CCSP: Cloud Security Operations (16%)

**Objective:** Define the cloud-audit-logging baseline a SOC monitors.

```bash
python3 - <<'PY'
baseline = ["control-plane API audit log (CloudTrail/Activity Log/Audit Logs)",
            "logs to a separate, append-only account/project",
            "alert on: root/owner use, IAM policy change, disabled logging",
            "retention per compliance (e.g., 1 year hot, longer cold)"]
for b in baseline: print("-", b)
PY
```

**Expected result:** the audit-logging and alerting baseline for cloud
operations — the monitoring foundation of Domain 5.

**Negative test:** store audit logs in the same account they record; an attacker
with access deletes them — isolate logs in a separate, append-only location.

**Cleanup:** none.

### Lab 6.6 — CCSP: Legal, Risk and Compliance (13%)

**Objective:** Reason about data residency and jurisdiction for a region choice.

```bash
python3 - <<'PY'
data = {"EU customer PII":"store in EU region (GDPR + adequacy)",
        "US health data":"HIPAA-eligible region + BAA with provider",
        "Public web assets":"any region (no residency constraint)"}
for d,rule in data.items(): print(f"{d:20} -> {rule}")
PY
```

**Expected result:** each data type mapped to a residency/jurisdiction rule —
the legal-and-compliance reasoning (GDPR, HIPAA, BAAs, data sovereignty) of
Domain 6.

**Negative test:** pick a cloud region purely on latency or price for regulated
data; **data residency and jurisdiction** can override both.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

CCSP is ISC2's vendor-neutral cloud-security credential, co-created with the
Cloud Security Alliance: six domains weighted 17/20/17/17/16/13 (with a new
outline arriving 1 August 2026), organized around the shared-responsibility
model and centered on cloud data security and key management. It sits above the
encyclopedia's provider-specific cloud volumes at the principle level.

- [ ] I can list the six CCSP domains and their weights.
- [ ] I can place the shared-responsibility boundary across IaaS/PaaS/SaaS.
- [ ] I can encrypt data under a customer-held key and design tiered SG rules.
- [ ] I can reason about data residency and JWT verification.
- [ ] I completed Labs 6.1–6.6 including each negative test.
