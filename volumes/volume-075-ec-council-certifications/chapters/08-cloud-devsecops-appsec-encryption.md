# Chapter 08: Cloud, DevSecOps, Application Security, and Encryption

## Learning Objectives

- Secure cloud workloads (CCSE).
- Embed security into the pipeline (ECDE / DevSecOps).
- Build secure applications (CASE .NET / Java).
- Apply cryptography correctly (ECES).
- Complete a walkthrough for each domain.

## Theory and Architecture

This chapter covers EC-Council's build-and-run security tracks. The **Certified Cloud Security
Engineer (CCSE)** validates securing **multi-cloud** environments — identity, network, data, and
platform controls under the **shared responsibility model** across AWS/Azure/GCP. The **Certified
DevSecOps Engineer (ECDE)** validates embedding security into **CI/CD** — shifting left with IaC
scanning, dependency and secrets checks, and automated guardrails so vulnerabilities are caught
before release. The **Certified Application Security Engineer (CASE, in .NET and Java editions)**
validates **secure software development** — building security into requirements, design, coding, and
testing (input validation, authentication, secure APIs). The **Certified Encryption Specialist
(ECES)** validates applied **cryptography** — symmetric/asymmetric algorithms, hashing, PKI, and
correct use. Together they secure the modern build-and-run lifecycle from code to cloud. This chapter
teaches each with a hands-on defensive walkthrough (cloud guardrails, pipeline scanning, secure
coding, and applied crypto).

## Design Considerations

Know the **shared responsibility** boundary (CCSE). **Shift security left** with automated pipeline
checks (ECDE). Build security into the **SDLC**, not bolted on (CASE). Use **standard, current**
cryptography correctly — never roll your own (ECES). Automate so security scales with delivery.

## Implementation and Automation

The labs set a cloud guardrail, scan a pipeline, apply a secure-coding check, and use crypto.

## Validation and Troubleshooting

Confirm the build-and-run map:

```text
CCSE = multi-cloud security + shared responsibility. ECDE = DevSecOps (IaC/dependency/secrets scanning, guardrails).
CASE (.NET/Java) = secure SDLC (validation/authn/secure APIs). ECES = applied cryptography (symmetric/asymmetric/hash/PKI).
```

Common pitfalls: bolting security on **after** release (expensive, incomplete); and misusing crypto
(custom algorithms, ECB mode, no salt).

## Security and Best Practices

Know the cloud **shared responsibility** line, **shift left** with automated checks, build security
into the **SDLC**, and use **standard cryptography** correctly. Automate guardrails. All work is
defensive.

## Hands-On Lab

Build-and-run walkthroughs. **Shared prerequisites** — Linux with `python3`, `openssl`, in a lab.
**Cost:** none.

### Lab 8.1 — CCSE: enforce a cloud guardrail

**Objective:** Prevent a risky config.

```python
python3 - <<'PY'
resources=[{"type":"storage","public":True},{"type":"db","encrypted":False},{"type":"vm","mfa_admin":True}]
violations=[]
for r in resources:
    if r.get("public"): violations.append(f"{r['type']} is public")
    if r.get("encrypted") is False: violations.append(f"{r['type']} unencrypted")
print("guardrail violations:", violations)
print("CCSE: deny public storage + require encryption (shared responsibility = customer owns config)")
PY
```

**Expected result:** the guardrail flags **public storage and an unencrypted DB** — CCSE cloud
control.

**Negative test:** assume the provider secures your config; the **customer** owns it — enforce
guardrails.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 8.2 — ECDE: scan the pipeline

**Objective:** Catch issues before release.

```python
python3 - <<'PY'
commit={"iac_public_bucket":True,"hardcoded_secret":"AKIA...LAB","vulnerable_dep":"lib@1.0 (CVE)"}
findings=[k for k,v in commit.items() if v]
print("pipeline findings:", findings)
print("ECDE: fail the build on secrets/misconfig/vuln deps -> never reaches production")
PY
```

**Expected result:** the pipeline flags a **secret, misconfig, and vulnerable dependency** — DevSecOps
guardrails (ECDE).

**Negative test:** merge without scanning; the hardcoded secret ships — **scan the pipeline** and
fail the build.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 8.3 — CASE: apply a secure-coding check

**Objective:** Validate input by default.

```python
python3 - <<'PY'
def safe_lookup(user_id):
    if not str(user_id).isdigit():           # input validation (allow-list)
        raise ValueError("invalid id")
    return f"SELECT * FROM users WHERE id = ?  -- param: {int(user_id)}"  # parameterized
print(safe_lookup("42"))
try: safe_lookup("1 OR 1=1")
except ValueError as e: print("rejected:", e)
print("CASE: validate input + parameterize queries -> injection resistant by design")
PY
```

**Expected result:** a valid ID accepted (parameterized) and an injection attempt **rejected** —
CASE secure coding.

**Negative test:** build the query with string concatenation; injection succeeds — **validate and
parameterize**.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 8.4 — ECES: apply cryptography correctly

**Objective:** Use standard crypto properly.

```bash
echo "sensitive" > secret.txt
openssl dgst -sha256 secret.txt                                       # hashing (integrity)
openssl enc -aes-256-cbc -pbkdf2 -salt -in secret.txt -out secret.enc -pass pass:LabKey  # AES w/ salt+KDF
openssl enc -d -aes-256-cbc -pbkdf2 -in secret.enc -pass pass:LabKey  # decrypt round-trip
```

**Expected result:** SHA-256 hashing and a salted **AES-256** encrypt/decrypt round-trip — correct
applied crypto (ECES).

**Negative test:** encrypt with ECB mode or no salt/KDF; patterns leak and it's weak — use **CBC/GCM
with salt and a KDF**.

**Rollback:** `rm -f secret.txt secret.enc`.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The build-and-run tracks secure the modern lifecycle: cloud (CCSE), pipeline (ECDE), application code
(CASE), and cryptography (ECES) — shared responsibility, shift-left scanning, secure SDLC, and correct
crypto.

- [ ] I can enforce a cloud guardrail (CCSE).
- [ ] I can scan the pipeline (ECDE).
- [ ] I can apply a secure-coding check (CASE).
- [ ] I can apply cryptography correctly (ECES).
- [ ] I completed Labs 8.1–8.4 including each negative test.
