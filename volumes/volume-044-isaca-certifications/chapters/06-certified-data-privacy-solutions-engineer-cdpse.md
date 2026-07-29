# Chapter 06: Certified Data Privacy Solutions Engineer (CDPSE)

## Learning Objectives

- Explain what CDPSE certifies and its engineering emphasis.
- List the four CDPSE domains (June 2025 refresh) and their exam weights.
- Apply privacy-by-design across governance, risk, data lifecycle, and engineering.
- Distinguish CDPSE from policy-only privacy certifications.
- Complete a per-domain walkthrough for each CDPSE domain.

## Theory and Architecture

The **Certified Data Privacy Solutions Engineer (CDPSE)** certifies the ability to
**implement privacy by design** — turning privacy requirements into technical
controls across the data lifecycle. Unlike policy-only privacy credentials, CDPSE
is **engineering-weighted**. The exam was **refreshed on 2 June 2025** from three
domains to **four**, and consists of **120 questions**:

| # | Domain | Weight |
|---|--------|--------|
| 1 | Privacy Governance | 20% |
| 2 | Privacy Risk Management and Compliance | 18% |
| 3 | Data Life Cycle Management | 23% |
| 4 | Privacy Engineering | 39% |

**Privacy Engineering (39%)** dominates by far — the technical implementation of
privacy is what distinguishes CDPSE.

## Design Considerations

CDPSE suits engineers, architects, and privacy technologists who **build** privacy
into systems. Emphasize Domain 4 (Privacy Engineering) — encryption,
de-identification, minimization, and privacy-preserving techniques — and treat
governance, risk/compliance, and the data lifecycle as the requirements that
engineering satisfies. CDPSE complements **CISM/CRISC** (management/risk) and maps
to regulations like **GDPR** and **CCPA**.

## Implementation and Automation

The labs below make each domain concrete: a privacy governance/role mapping (D1),
a compliance mapping to a regulation (D2), a data-lifecycle/retention model (D3),
and hands-on privacy engineering — hashing/pseudonymization and minimization (D4).

## Validation and Troubleshooting

Confirm the CDPSE blueprint before studying:

```text
isaca.org > Credentialing > CDPSE > Exam Content Outline:
  - four domains and weights (20/18/23/39), 120 questions, refreshed 2 Jun 2025
  - three years of privacy/data-protection experience
```

Common pitfalls: studying the **retired three-domain** outline; treating CDPSE as
a policy exam (it is **engineering**-weighted); and confusing **anonymization**
(irreversible) with **pseudonymization** (reversible with a key).

## Security and Best Practices

Engineer privacy in: **minimize** data collection, **encrypt** at rest and in
transit, **pseudonymize/anonymize** where possible, enforce **retention and
deletion**, and honor **data-subject rights**. Map controls to **GDPR/CCPA** and
privacy frameworks. Renew via CPE.

## References and Knowledge Checks

- isaca.org: *CDPSE* Exam Content Outline and review manual; GDPR; NIST Privacy Framework.

**Knowledge checks**

1. Which CDPSE domain dominates, and why?
2. What changed in the June 2025 CDPSE refresh?
3. What is the difference between anonymization and pseudonymization?

## Hands-On Lab

Per-topic walkthroughs — **one lab for every weighted CDPSE domain**.

**Shared prerequisites** — a Linux shell with `python3` and `openssl`.
**Cost:** none.

### Lab 6.1 — CDPSE D1: Privacy Governance (20%)

**Objective:** Map privacy roles and accountability (controller vs processor).

```bash
python3 - <<'PY'
roles = {"Controller":"determines purposes/means of processing (accountable)",
         "Processor":"processes on the controller's behalf (bound by contract)",
         "DPO":"oversees compliance, advises, contact point"}
for r,d in roles.items(): print(f"{r:11}: {d}")
PY
```

**Expected result:** the privacy roles and their accountability — the governance
foundation (Domain 1) that assigns responsibility for processing.

**Negative test:** treat a processor as accountable for purpose; the
**controller** determines purpose and bears accountability — know the roles.

**Cleanup:** none.

### Lab 6.2 — CDPSE D2: Privacy Risk Management and Compliance (18%)

**Objective:** Map a processing activity to its legal basis and controls.

```bash
python3 - <<'PY'
activities = {"Marketing emails":"legal basis: consent -> opt-in + easy withdrawal",
              "Payroll processing":"legal basis: contract/legal obligation",
              "Fraud detection":"legal basis: legitimate interest -> LIA + safeguards"}
for act,basis in activities.items(): print(f"{act:20} -> {basis}")
PY
```

**Expected result:** each processing activity mapped to a legal basis and control
— the compliance/risk mapping of Domain 2 (e.g., GDPR Art. 6).

**Negative test:** rely on consent for everything; different activities have
different **legal bases** — match each correctly.

**Cleanup:** none.

### Lab 6.3 — CDPSE D3: Data Life Cycle Management (23%)

**Objective:** Define retention and deletion across the data lifecycle.

```bash
python3 - <<'PY'
lifecycle = {"Collect":"minimize to purpose","Store":"encrypt + access control",
             "Use":"purpose limitation","Share":"contracts + transfer safeguards",
             "Retain":"retention schedule per data type","Delete":"secure deletion at end of retention"}
for phase,rule in lifecycle.items(): print(f"{phase:8}: {rule}")
PY
```

**Expected result:** a privacy control per lifecycle phase, ending in deletion —
the data-lifecycle management of Domain 3.

**Negative test:** keep personal data indefinitely "just in case"; **retention
limitation** requires deletion at end of purpose — schedule it.

**Cleanup:** none.

### Lab 6.4 — CDPSE D4: Privacy Engineering (39%)

**Objective:** Pseudonymize a direct identifier (privacy-by-design in practice).

```bash
python3 - <<'PY'
import hashlib, hmac
KEY=b"org-pepper-key"           # kept separate -> pseudonymization (reversible via mapping), not anonymization
def pseudonymize(email): return hmac.new(KEY, email.encode(), hashlib.sha256).hexdigest()[:16]
for e in ["alice@example.com","bob@example.com"]:
    print(f"{e:20} -> token {pseudonymize(e)}")
print("Note: with the key/mapping this is PSEUDONYMIZATION; drop the mapping for anonymization.")
PY
```

**Expected result:** stable pseudonymous tokens replacing emails — hands-on
privacy engineering (Domain 4), CDPSE's largest and most technical domain.

**Negative test:** call keyed pseudonymization "anonymization"; it is reversible
with the key — true anonymization removes any path back to the individual.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

CDPSE certifies privacy-by-design engineering: four domains weighted 20/18/23/39
(June 2025 refresh), dominated by Privacy Engineering. It turns privacy
governance, risk/compliance, and data-lifecycle requirements into technical
controls — minimization, encryption, pseudonymization, and retention — mapped to
GDPR/CCPA.

- [ ] I can list the four CDPSE domains and their weights.
- [ ] I can map privacy roles and legal bases for processing.
- [ ] I can define lifecycle retention/deletion controls.
- [ ] I can pseudonymize an identifier and explain vs anonymization.
- [ ] I completed Labs 6.1–6.4 including each negative test.
