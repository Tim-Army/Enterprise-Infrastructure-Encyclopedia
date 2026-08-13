# Chapter 08: Certified Secure Software Lifecycle Professional (CSSLP)

## Learning Objectives

- Explain what CSSLP certifies and who should pursue it.
- List the eight CSSLP domains and their exam weights.
- Describe how CSSLP maps security onto every phase of the software development lifecycle.
- Apply secure-SDLC thinking: requirements, design, implementation, testing, and supply chain.
- Complete a per-domain walkthrough for each CSSLP domain.

## Theory and Architecture

The **Certified Secure Software Lifecycle Professional (CSSLP)** certifies that
its holder can **build security into software** at every phase of the SDLC —
not bolt it on afterward. It is aimed at developers, architects, application-
security engineers, and DevSecOps practitioners, and it requires **four years**
of experience in the SDLC. Where CISSP Domain 8 touches software security
broadly, CSSLP goes deep across the whole lifecycle.

The exam is **125 items in 3 hours**, pass mark **700/1000**. The outline
effective **15 September 2023** weights the domains:

| # | Domain | Weight |
|---|--------|--------|
| 1 | Secure Software Concepts | 12% |
| 2 | Secure Software Lifecycle Management | 11% |
| 3 | Secure Software Requirements | 13% |
| 4 | Secure Software Architecture and Design | 15% |
| 5 | Secure Software Implementation | 14% |
| 6 | Secure Software Testing | 14% |
| 7 | Secure Software Deployment, Operations, Maintenance | 11% |
| 8 | Secure Software Supply Chain | 10% |

The domains follow the SDLC in order — concepts and lifecycle governance, then
requirements → design → implementation → testing → deployment/operations, closed
by the increasingly critical **software supply chain** domain.

## Design Considerations

CSSLP suits anyone accountable for **application security** who wants to prove
lifecycle-wide competence rather than point tooling. It complements the
encyclopedia's **automation and platform-engineering volumes** (IX, VIII) where
CI/CD and supply-chain controls live. Emphasize **Domain 4 (design, 15%)** —
threat modeling and secure design patterns prevent whole vulnerability classes
before a line is written — and take the newer **Supply Chain (Domain 8)**
seriously: dependency, build-integrity, and provenance attacks (SolarWinds-class)
are now core exam content.

## Implementation and Automation

The labs below use portable developer tooling to make each domain concrete: a
misuse-case (concepts), a security gate in a pipeline (lifecycle), a security
requirement (requirements), a threat-model enumeration (design), input
validation and secrets handling (implementation), a security test (testing), a
hardened deployment config (deployment/ops), and a dependency/SBOM integrity
check (supply chain).

## Validation and Troubleshooting

Confirm the CSSLP blueprint before studying:

```text
isc2.org > Certifications > CSSLP > Exam Outline:
  - eight domains and weights (12/11/13/15/14/14/11/10, eff 15 Sep 2023)
  - 125 items, 3 hours, 700/1000
  - four years of SDLC experience
```

Common pitfalls: treating CSSLP as a **coding** exam (it is about *process and
design*, language-agnostic); skipping **threat modeling** (the highest-leverage
Domain 4 skill); and underestimating **supply chain** as "just dependencies" —
it now spans provenance, build integrity, and SBOMs.

## Security and Best Practices

Shift security **left**: model threats at design, validate all input, manage
secrets outside code, and gate the pipeline with SAST/DAST/SCA. Adopt a
recognized secure-SDLC framework (**NIST SSDF SP 800-218**, **OWASP SAMM**) and
generate an **SBOM** for every build. Renew CSSLP with CPE and AMF.

## References and Knowledge Checks

- isc2.org: *CSSLP* page and Exam Outline; OWASP (Top 10, ASVS, SAMM); NIST SSDF (SP 800-218).

**Knowledge checks**

1. Which CSSLP domain is heaviest, and why is design so high-leverage?
2. How does CSSLP differ from a language-specific secure-coding course?
3. What does the Secure Software Supply Chain domain cover beyond dependencies?

## Hands-On Lab

Per-topic walkthroughs — **one lab for every weighted CSSLP domain**.

**Shared prerequisites** — a Linux shell with `python3`, `openssl`, and
`sha256sum`. **Cost:** none.

### Lab 8.1 — CSSLP: Secure Software Concepts (12%)

**Objective:** Write a misuse case alongside a use case (abuse thinking).

```bash
python3 - <<'PY'
use_case  = "User uploads a profile photo (JPEG/PNG, <5MB)"
misuse    = ["upload a .php webshell renamed .jpg",
             "upload a 5GB file (DoS)",
             "path traversal in filename ../../etc"]
print("USE CASE :", use_case)
for m in misuse: print(" MISUSE  :", m, "-> control: validate type/size/name server-side")
PY
```

**Expected result:** a use case paired with concrete misuse cases and controls —
the security-mindset (assume abuse) that underpins CSSLP concepts.

**Negative test:** design only for the happy path; attackers target the misuse
cases — enumerate them explicitly.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 8.2 — CSSLP: Secure Software Lifecycle Management (11%)

**Objective:** Define pipeline security gates by SDLC phase.

```bash
python3 - <<'PY'
gates = {"commit":"secret scan + SAST","build":"SCA (dependency CVEs) + SBOM",
         "test":"DAST + security unit tests","release":"sign artifact + provenance",
         "deploy":"policy check + config scan"}
for phase,gate in gates.items(): print(f"{phase:7} -> {gate}")
PY
```

**Expected result:** a security gate at each pipeline stage — the secure-SDLC
governance CSSLP Domain 2 manages (aligned to NIST SSDF).

**Negative test:** run one security scan at the end; late findings are expensive
— gate every phase.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 8.3 — CSSLP: Secure Software Requirements (13%)

**Objective:** Derive a testable security requirement from a policy.

```bash
python3 - <<'PY'
policy = "Protect authentication credentials"
requirements = ["passwords stored only as salted Argon2/bcrypt hashes",
                "enforce MFA for privileged accounts",
                "lock account after 10 failed attempts in 15 min"]
print("Policy:", policy)
for r in requirements: print(" REQ (testable):", r)
PY
```

**Expected result:** a policy decomposed into specific, testable security
requirements — the traceable requirements CSSLP Domain 3 produces.

**Negative test:** write "the system shall be secure"; untestable requirements
cannot be verified — make each measurable.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 8.4 — CSSLP: Secure Software Architecture and Design (15%)

**Objective:** Enumerate threats with STRIDE against a data flow.

```bash
python3 - <<'PY'
stride = {"Spoofing":"authenticate endpoints (mTLS/OIDC)",
          "Tampering":"integrity (signatures/HMAC)",
          "Repudiation":"audit logging",
          "Information disclosure":"encryption + least privilege",
          "Denial of service":"rate limiting + quotas",
          "Elevation of privilege":"authorization checks + sandboxing"}
for threat,control in stride.items(): print(f"{threat:24} -> {control}")
PY
```

**Expected result:** the six STRIDE threat categories each mapped to a
mitigating control — the threat-modeling core of CSSLP's heaviest domain.

**Negative test:** review code for bugs without a threat model; design flaws (not
just bugs) cause the worst breaches — model threats first.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 8.5 — CSSLP: Secure Software Implementation (14%)

**Objective:** Show safe secret handling and output encoding.

```bash
python3 - <<'PY'
import os, html
secret = os.environ.get("DB_PASSWORD", "<from-vault-not-source>")   # never hard-code
print("secret loaded from environment/vault, not source:", secret[:4]+"…")
untrusted = "<script>alert(1)</script>"
print("output-encoded:", html.escape(untrusted))   # neutralize XSS on output
PY
```

**Expected result:** the secret sourced from the environment (not code) and the
untrusted string HTML-encoded to `&lt;script&gt;…` — two implementation controls
(secrets management, output encoding) CSSLP Domain 5 tests.

**Negative test:** hard-code a password or echo untrusted input verbatim; the
first leaks in source control, the second is stored/reflected XSS.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 8.6 — CSSLP: Secure Software Testing (14%)

**Objective:** Write a security test asserting a control works (negative test).

```bash
python3 - <<'PY'
def transfer(amount):
    if amount <= 0: raise ValueError("amount must be positive")   # the control
    return f"transferred {amount}"
tests = [(100,"pass"),(-50,"must reject"),(0,"must reject")]
for amt,expect in tests:
    try: print(amt, "->", transfer(amt), "(expected", expect+")")
    except ValueError as e: print(amt, "-> REJECTED:", e, "(expected", expect+")")
PY
```

**Expected result:** 100 succeeds, −50 and 0 are rejected — a security test
proving input validation holds, the evidence CSSLP Domain 6 requires.

**Negative test:** test only valid inputs; security tests must assert that
*invalid* inputs are **rejected**.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 8.7 — CSSLP: Secure Software Deployment, Operations, Maintenance (11%)

**Objective:** Harden a deployment config and plan patch cadence.

```bash
python3 - <<'PY'
hardening = {"debug":"false in production","default_creds":"removed",
             "TLS":"1.2+ only, HSTS on","error_pages":"generic (no stack traces)",
             "patching":"critical <=7 days, high <=30 days"}
for k,v in hardening.items(): print(f"{k:14}: {v}")
PY
```

**Expected result:** a production-hardening checklist and patch SLAs — the
deploy-and-operate controls of CSSLP Domain 7.

**Negative test:** ship with `debug=true` or verbose stack traces; both leak
internals to attackers — disable in production.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 8.8 — CSSLP: Secure Software Supply Chain (10%)

**Objective:** Verify artifact integrity and reason about an SBOM.

```bash
echo "app-binary v1.0" > app.bin
sha256sum app.bin | tee app.bin.sha256                 # publish a known-good digest
sha256sum -c app.bin.sha256 && echo "SUPPLY-CHAIN CHECK: artifact matches published digest"
echo "SBOM lists every dependency + version -> scan against CVE feeds + verify provenance"
```

**Expected result:** the artifact verified against its published digest, plus the
SBOM/provenance concept — the build-integrity and dependency controls of the
supply-chain domain (Domain 8).

**Negative test:** deploy an artifact without verifying its digest or provenance;
a tampered build (SolarWinds-class) passes unnoticed — verify integrity and
provenance.

**Rollback:** `rm -f app.bin app.bin.sha256`

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

CSSLP certifies lifecycle-wide software security: eight domains weighted
12/11/13/15/14/14/11/10 (effective 15 September 2023) tracing the SDLC from
concepts and requirements through design, implementation, testing, deployment,
and the software supply chain. It is language-agnostic and process-centered,
with threat modeling (Domain 4) and supply-chain integrity (Domain 8) as its
highest-leverage skills.

- [ ] I can list the eight CSSLP domains and their weights.
- [ ] I can write misuse cases and a STRIDE threat model.
- [ ] I can derive testable requirements and security tests.
- [ ] I can verify artifact integrity and explain SBOM/provenance.
- [ ] I completed Labs 8.1–8.8 including each negative test.
