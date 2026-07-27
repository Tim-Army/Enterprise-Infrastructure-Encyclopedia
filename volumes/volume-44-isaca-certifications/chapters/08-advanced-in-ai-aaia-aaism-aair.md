# Chapter 08: Advanced in AI — AAIA, AAISM, and AAIR

## Learning Objectives

- Explain ISACA's Advanced in AI family and how it extends CISA, CISM, and CRISC.
- List the AAIA, AAISM, and AAIR domains and the AAISM/AAIA weights.
- Apply AI governance, audit, security-management, and risk to AI systems.
- Understand the AI-specific risks and controls these credentials certify.
- Complete a per-domain walkthrough for every domain of all three credentials.

## Theory and Architecture

ISACA's newest credentials extend its core disciplines into **artificial
intelligence** — a direct response to AI governance becoming a board-level
concern (mirroring the ISC2 AI Security cert in development and CompTIA SecAI+):

- **AAIA — Advanced in AI Audit** (extends **CISA**). **3 domains** (scenario-
  based): **AI Governance & Risk (33%)**, **AI Operations** (the heaviest), and
  **AI Auditing Tools & Techniques**. For auditors assuring AI systems.
- **AAISM — Advanced in AI Security Management** (extends **CISM**). **3 domains,
  90 questions**: **AI Governance and Program Management (31%)**, **AI Risk
  Management (31%)**, and **AI Technologies and Controls (38%)**. For security
  managers securing AI.
- **AAIR — Advanced in AI Risk** (extends **CRISC**; launched 2026). **3
  domains**: **AI Risk Governance and Framework Integration**, **AI Risk Program
  Management**, and **AI Life Cycle Risk Management**. For risk professionals
  governing AI risk.

Each builds on an active base certification (CISA/CISM/CRISC) and applies its
discipline to the specific risks and controls of AI.

## Design Considerations

Choose by **base discipline**: CISA holders auditing AI take **AAIA**, CISM
holders securing AI take **AAISM**, and CRISC holders governing AI risk take
**AAIR**. The common thread is **AI-specific** governance and control — model
lifecycle risk, data provenance, bias/ethics, regulatory alignment (e.g., the
**EU AI Act** and the **NIST AI RMF**), and the security of models and pipelines.
Because the family is new, verify each outline on isaca.org.

## Implementation and Automation

The labs below model each domain's decisions: AI policy, operations audit, and
audit technique (AAIA); AI security governance, AI risk, and AI controls (AAISM);
and AI risk governance, program, and lifecycle (AAIR) — the artifacts these
credentials certify.

## Validation and Troubleshooting

Confirm the blueprints before studying:

```text
isaca.org > Credentialing > AAIA | AAISM | AAIR > Exam Content Outline:
  - AAIA (3 domains; AI Governance & Risk 33%), AAISM (3; 31/31/38, 90 Q), AAIR (3)
  - each extends an active base cert (CISA / CISM / CRISC)
```

Common pitfalls: pursuing an Advanced in AI credential without the **base cert**
context; and treating AI risk as ordinary IT risk — AI adds **model, data, and
lifecycle** risks (drift, bias, poisoning, provenance) that need specific
controls.

## Security and Best Practices

Govern AI to recognized frameworks (**NIST AI RMF**, **ISO/IEC 42001**, the **EU
AI Act**): inventory AI systems, assess **model and data risk** across the
lifecycle, require **provenance** and testing, embed **ethics/bias** review, and
monitor deployed models for **drift**. Treat the model's data sources and tools
as attack surface. Renew via CPE.

## References and Knowledge Checks

- isaca.org: *AAIA*, *AAISM*, *AAIR* Exam Content Outlines; NIST AI RMF; ISO/IEC 42001; EU AI Act.

**Knowledge checks**

1. Which base certification does each Advanced in AI credential extend?
2. What AI-specific risks distinguish AI risk from ordinary IT risk?
3. Which frameworks anchor AI governance?

## Hands-On Lab

Per-topic walkthroughs — **one lab for every domain of all three credentials**.

**Shared prerequisites** — a Linux shell with `python3`. **Cost:** none.

### AAIA — Advanced in AI Audit

### Lab 8.1 — AAIA: AI Governance & Risk (33%)

**Objective:** Map an AI risk to a policy control and regulation.

```bash
python3 - <<'PY'
gov = {"Biased model output":"fairness testing + human review (EU AI Act high-risk)",
       "Untraceable decisions":"explainability + audit logging",
       "Unapproved model in prod":"AI inventory + approval gate"}
for risk,ctrl in gov.items(): print(f"{risk:24} -> {ctrl}")
PY
```

**Expected result:** AI risks mapped to policy controls and regulation — the
governance-and-risk domain that leads AAIA.

**Negative test:** govern AI with generic IT policy only; AI needs **specific**
controls (bias, explainability, inventory).

**Cleanup:** none.

### Lab 8.2 — AAIA: AI Operations (heaviest)

**Objective:** Audit an AI system in operation (monitoring and drift).

```bash
python3 - <<'PY'
checks = ["Is model performance monitored (accuracy/drift) in production?",
          "Are inputs/outputs logged for audit and investigation?",
          "Is there a rollback for a misbehaving model?",
          "Are retraining data and approvals documented?"]
for c in checks: print("audit ->", c)
PY
```

**Expected result:** an AI-operations audit checklist (monitoring, logging,
rollback, retraining governance) — AAIA's heaviest domain.

**Negative test:** audit only pre-deployment; AI risk is **ongoing** (drift,
data changes) — audit operations too.

**Cleanup:** none.

### Lab 8.3 — AAIA: AI Auditing Tools & Techniques

**Objective:** Scope an AI audit and gather model/pipeline evidence.

```bash
python3 - <<'PY'
plan = {"Scope":"which models, data, and decisions are in scope",
        "Evidence":"model cards, data lineage, test results, approval records",
        "Technique":"bias tests, reproducibility checks, control walkthroughs",
        "Report":"findings + risk ratings + recommendations"}
for k,v in plan.items(): print(f"{k:9}: {v}")
PY
```

**Expected result:** an AI-audit method (scope → evidence → technique → report) —
the mechanics domain of AAIA.

**Negative test:** audit an AI system with no model cards or data lineage; require
**provenance evidence** to audit it credibly.

**Cleanup:** none.

### AAISM — Advanced in AI Security Management

### Lab 8.4 — AAISM: AI Governance and Program Management (31%)

**Objective:** Stand up an AI security program element.

```bash
python3 - <<'PY'
program = {"AI inventory":"catalog models, data, and their owners",
           "AI acceptable-use policy":"what AI may/may not be used for",
           "Security review gate":"threat-model AI systems before deployment"}
for k,v in program.items(): print(f"{k:24}: {v}")
PY
```

**Expected result:** AI security-program elements (inventory, policy, review gate)
— AAISM Domain 1.

**Negative test:** secure AI ad hoc; a **managed program** (inventory + policy +
gates) is what AAISM certifies.

**Cleanup:** none.

### Lab 8.5 — AAISM: AI Risk Management (31%)

**Objective:** Assess an AI-specific risk.

```bash
python3 - <<'PY'
airisks = {"Prompt injection":"input trust + tool permission limits",
           "Training-data poisoning":"data provenance + validation",
           "Model theft/extraction":"rate limits + access control + monitoring"}
for r,c in airisks.items(): print(f"{r:26} -> control: {c}")
PY
```

**Expected result:** AI-specific risks with controls — the AI risk management of
AAISM Domain 2.

**Negative test:** apply only generic infosec risk; AI adds **model/data/prompt**
risks — assess them explicitly.

**Cleanup:** none.

### Lab 8.6 — AAISM: AI Technologies and Controls (38%)

**Objective:** Select technical controls for an AI pipeline.

```bash
python3 - <<'PY'
controls = {"Model provenance":"signed models + verified sources",
            "Data pipeline":"integrity checks + access control",
            "Inference":"input validation, output filtering, rate limiting",
            "Tools/plugins":"least privilege for anything the model can invoke"}
for area,ctrl in controls.items(): print(f"{area:16} -> {ctrl}")
PY
```

**Expected result:** technical AI controls across provenance, pipeline, inference,
and tools — AAISM's heaviest domain.

**Negative test:** give an AI agent broad tool permissions; the model's tools are
its attack surface — apply **least privilege**.

**Cleanup:** none.

### AAIR — Advanced in AI Risk

### Lab 8.7 — AAIR: AI Risk Governance and Framework Integration

**Objective:** Integrate AI risk into enterprise risk management.

```bash
python3 - <<'PY'
print("Integrate AI risk into ERM: add AI risks to the enterprise register,")
print("map to NIST AI RMF / ISO 42001, and assign owners + appetite per AI risk category.")
PY
```

**Expected result:** AI risk plugged into the enterprise risk framework — AAIR
Domain 1.

**Negative test:** manage AI risk in a silo; integrate it into **ERM** so it is
governed like other enterprise risk.

**Cleanup:** none.

### Lab 8.8 — AAIR: AI Risk Program Management

**Objective:** Run recurring AI risk operations.

```bash
python3 - <<'PY'
ops = ["Periodic AI risk reviews","Third-party/vendor AI risk assessments",
       "Recurring control testing","KRI monitoring for AI (e.g., drift, incidents)"]
for o in ops: print("-", o)
PY
```

**Expected result:** the operational AI-risk program (reviews, third-party
assessments, control testing, KRIs) — AAIR Domain 2.

**Negative test:** assess AI risk once at launch; a **program** runs recurring
reviews — AI systems change.

**Cleanup:** none.

### Lab 8.9 — AAIR: AI Life Cycle Risk Management

**Objective:** Manage model risk across the lifecycle.

```bash
python3 - <<'PY'
lifecycle = {"Training":"data quality/provenance, bias assessment",
             "Validation":"performance + robustness testing",
             "Deployment":"approval gate + monitoring plan",
             "Monitoring":"drift, incidents, feedback",
             "Decommission":"retire safely, retain records"}
for phase,risk in lifecycle.items(): print(f"{phase:12}: manage -> {risk}")
PY
```

**Expected result:** model-risk controls at each lifecycle phase — the lifecycle
risk management of AAIR Domain 3.

**Negative test:** manage only deployment risk; model risk spans **training to
decommission** — govern the whole lifecycle.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

ISACA's Advanced in AI family extends its core disciplines into AI: **AAIA** (AI
audit, extends CISA), **AAISM** (AI security management, extends CISM; 31/31/38),
and **AAIR** (AI risk, extends CRISC). Each certifies AI-specific governance and
control — model/data/lifecycle risk, provenance, ethics, and regulatory alignment
(NIST AI RMF, ISO 42001, EU AI Act).

- [ ] I can match each Advanced in AI credential to its base certification.
- [ ] I can list the AAIA, AAISM, and AAIR domains and known weights.
- [ ] I can identify AI-specific risks and their controls.
- [ ] I can manage AI risk across the model lifecycle.
- [ ] I completed Labs 8.1–8.9 including each negative test.
