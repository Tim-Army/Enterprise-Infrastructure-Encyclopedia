# Chapter 09: Artificial Intelligence, Currency, and Career

## Learning Objectives

- Describe GIAC's Artificial Intelligence focus area (GMLE, GAIPS, GASAE, GOAA).
- Apply machine learning to a defensive security problem (GMLE).
- Reason about securing AI platforms and LLM pipelines (GAIPS).
- Keep GIAC credentials current and plan a career.
- Complete a walkthrough for AI and currency.

## Theory and Architecture

GIAC's newest focus area, **Artificial Intelligence**, certifies practitioners who apply and secure
AI. **GMLE (Machine Learning Engineer)** validates applying **machine learning to cybersecurity
challenges** — feature engineering, model selection, and evaluation for detection problems. **GAIPS
(AI Platform Security)** validates **auditing and securing generative-AI applications and LLM
development pipelines** — prompt-injection defense, data governance, and supply-chain security for
models. **GASAE (AI Security Automation Engineer)** validates applying AI/automation across
offensive, defensive, and cloud operations. **GOAA (Offensive AI Analyst)** validates *authorized*
offensive-AI technique. These sit alongside the established focus areas and reflect the industry's
shift toward AI-driven security. On **currency**: GIAC certifications are valid **four years** and
are renewed by continuing professional education (CPE) or re-examination, and the program adds
certifications frequently — so verifying the current catalog on giac.org is an ongoing task. This
closing chapter teaches AI defensively and turns the volume into a durable career and renewal plan.

> **Scope.** The AI-offensive material (GOAA/GASAE) is treated as **authorized methodology** only,
> consistent with Chapter 4 — no operational attack payloads.

## Design Considerations

Apply ML where it beats rules (high-volume, fuzzy detection) and keep it **explainable** and
**evaluated** (GMLE). Secure the **AI supply chain** — models, data, and pipelines — and defend
against **prompt injection** (GAIPS). Automate with guardrails (GASAE). Renew credentials **before**
the four-year expiry; re-verify the catalog as GIAC adds certifications. Match certs to your
**career** direction.

## Implementation and Automation

The labs build a simple ML detector, reason about LLM-pipeline risks, and plan currency.

## Validation and Troubleshooting

Confirm the AI/currency map:

```text
GMLE = ML applied to security. GAIPS = securing GenAI apps + LLM pipelines (prompt injection, data governance).
GASAE = AI/automation across red/blue/cloud. GOAA = authorized offensive AI. Currency: 4-year validity, CPE or re-exam; catalog grows.
```

Common pitfalls: deploying an **unevaluated** ML model (false positives at scale); and ignoring
**prompt injection / data poisoning** when adding an LLM feature.

## Security and Best Practices

Use ML where it helps, keep it **evaluated and explainable**, secure the **AI supply chain**, and
defend LLM apps against injection. Renew credentials before expiry and re-check the catalog. All AI
work here is defensive or authorized.

## Hands-On Lab

AI and currency walkthroughs. **Shared prerequisites** — Linux with `python3`. **Cost:** none.

### Lab 9.1 — GMLE: a simple defensive ML detector

**Objective:** Apply ML thinking to detection.

```python
python3 - <<'PY'
# Threshold "model": classify logins as anomalous by simple features (illustrative GMLE reasoning)
samples=[{"hour":3,"failed":8,"label":"?"},{"hour":14,"failed":0,"label":"?"}]
def score(s): return (s["hour"]<6)*1 + (s["failed"]>=5)*2   # off-hours + many failures
for s in samples:
    s["label"]="anomalous" if score(s)>=2 else "normal"
    print(f"hour={s['hour']:>2} failed={s['failed']:>2} -> {s['label']} (score {score(s)})")
print("GMLE: features + a scoring model + evaluation; a real model is trained and measured (precision/recall)")
PY
```

**Expected result:** the off-hours, high-failure login flagged **anomalous** — ML applied to
detection (GMLE).

**Negative test:** ship a model without measuring **precision/recall**; it may flag everything —
**evaluate** before deploying.

**Cleanup:** none.

### Lab 9.2 — GAIPS: assess an LLM pipeline risk

**Objective:** Secure a GenAI application.

```python
python3 - <<'PY'
risks={"prompt injection":"validate/segment untrusted input; don't let it reach tools/secrets",
       "data poisoning":"govern training/RAG data sources + provenance",
       "model supply chain":"verify model signatures/hashes before deploy",
       "sensitive data leakage":"output filtering + least-privilege tool access"}
for r,fix in risks.items(): print(f"{r:22}: {fix}")
print("GAIPS: audit the whole LLM pipeline — input, data, model, output")
PY
```

**Expected result:** the LLM-pipeline risks with **mitigations** — the GAIPS audit view.

**Negative test:** connect an LLM directly to privileged tools with unfiltered user input; **prompt
injection** becomes command execution — segment and validate.

**Cleanup:** none.

### Lab 9.3 — Plan currency and career

**Objective:** Keep credentials and skills current.

```python
python3 - <<'PY'
routine={"Validity":"GIAC certs valid 4 years — renew via CPE or re-exam before expiry",
         "Catalog":"re-verify codes/new certs on giac.org (AI area grows fast)",
         "CyberLive":"keep hands-on skills sharp on authorized labs",
         "Career":"stack a focus area (e.g., GSEC->GCIH->GCFA for DFIR) toward your role"}
for k,v in routine.items(): print(f"- {k}: {v}")
PY
```

**Expected result:** a currency-and-career routine — renewals, catalog checks, hands-on practice, and
a focus-area stack.

**Negative test:** let a cert lapse past **four years**; it's no longer current — renew via **CPE or
re-exam** ahead of expiry.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

GIAC's AI focus area (GMLE, GAIPS, GASAE, GOAA) certifies applying and securing AI; credentials are
valid four years and renewed by CPE or re-exam, and the catalog grows — so an evergreen routine of
verifying codes, practicing hands-on, and stacking a focus area keeps you current.

- [ ] I can build a simple defensive ML detector (GMLE).
- [ ] I can assess LLM-pipeline risks (GAIPS).
- [ ] I can plan four-year renewal and catalog checks.
- [ ] I can stack a focus area toward my career.
- [ ] I completed Labs 9.1–9.3 including each negative test.
