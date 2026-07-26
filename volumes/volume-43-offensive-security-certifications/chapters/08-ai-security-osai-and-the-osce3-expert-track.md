# Chapter 08: AI Security (OSAI) and the OSCE³ Expert Track

## Learning Objectives

- Explain the new AI-security credential: OSAI (AI-300, OffSec AI Red Teamer).
- Describe AI red-teaming areas: prompt injection, adversarial ML, and the AI supply chain.
- Explain the OSCE³ expert designation and how it is earned.
- Practice AI-attack methodology and defenses conceptually and safely.
- Complete per-topic walkthroughs for the OSAI areas and the expert track.

## Theory and Architecture

OffSec's newest track addresses securing **AI systems**:

- **OSAI (OffSec AI Red Teamer, AI-300)** — a new credential for **red-teaming AI
  and machine-learning systems**: **prompt injection** and jailbreaks against
  LLMs, **adversarial machine learning** (evasion, poisoning, model extraction),
  and **AI supply-chain** risks (models, datasets, plugins/tools). It uses the
  three-year **"+" renewal**. Its emergence tracks the industry-wide push to
  secure AI (echoed in the ISC2 AI Security cert in development and the CompTIA
  SecAI+).

The chapter also covers the **OSCE³** expert designation:

- **OSCE³ (OffSec Certified Expert 3)** — not a separate exam but an **umbrella**
  earned by holding all three core 300-level credentials: **OSEP** (PEN-300),
  **OSWE** (WEB-300), and **OSED** (EXP-301). It marks expert breadth across
  advanced pentesting, web, and exploit development.

## Design Considerations

**OSAI** suits security engineers working with LLMs and ML pipelines; the durable
skill is understanding **where AI systems fail** (untrusted input reaching a model
or its tools, poisoned training data, unverified model provenance) so you can
**defend** them. Pursue **OSCE³** by planning the three 300-level courses as a set
— they share the "advanced, hands-on" bar and together certify expert breadth.

## Implementation and Automation

The labs below reason about AI attacks and defenses **conceptually and safely** —
they do not attack any live model or service, and each pairs the risk with its
control (input/output handling, provenance, least-privilege tool access). The
OSCE³ lab maps the path to the umbrella.

## Validation and Troubleshooting

Confirm the credential and designation on offsec.com:

```text
offsec.com/courses:
  - AI-300 -> OSAI (AI Red Teamer: prompt injection, adversarial ML, AI supply chain) — "+" renewal
  - OSCE3 = OSEP (PEN-300) + OSWE (WEB-300) + OSED (EXP-301)
```

Common pitfalls: treating **prompt injection** as a content-filter problem (it is
an **input-trust and tool-permission** problem); and assuming a downloaded model
is safe (verify **provenance**).

## Security and Best Practices

Defend AI systems with the same principles as any system: **never trust input**
(treat all model input, including retrieved content, as untrusted), **constrain
tool/plugin permissions** (least privilege for anything the model can invoke),
**validate output** before acting on it, **verify model and dataset provenance**,
and **monitor** for anomalous prompts and outputs. Map risks to the emerging
frameworks (OWASP LLM Top 10, MITRE ATLAS).

## References and Knowledge Checks

- offsec.com: *AI-300 (OSAI)* course page; OWASP Top 10 for LLM Applications; MITRE ATLAS.

**Knowledge checks**

1. What three areas does OSAI red-teaming cover?
2. Why is prompt injection an input-trust and tool-permission problem?
3. How is OSCE³ earned?

## Hands-On Lab

Per-topic walkthroughs — **concept and defense only; no live model or service is
attacked.**

**Shared prerequisites** — a shell with `python3`. **Cost:** none.

### OSAI — AI Red Teaming

### Lab 8.1 — OSAI: prompt injection (concept and defense)

**Objective:** Understand prompt injection and its controls.

```bash
python3 - <<'PY'
print("Prompt injection: untrusted content (a webpage, a document, a tool result) contains")
print("instructions the model may follow, overriding the developer's intent.")
print("Defense: treat retrieved/user content as DATA not instructions; constrain tool permissions;")
print("validate/whitelist actions; keep a human approval for side effects.")
PY
```

**Expected result:** what prompt injection is and the input-trust/tool-permission
defenses — the core OSAI concept, framed for defense.

**Negative test:** rely on a keyword content filter; injection hides in encodings
and phrasing — the fix is **not trusting** retrieved content as instructions.

**Cleanup:** none.

### Lab 8.2 — OSAI: adversarial machine learning (concept)

**Objective:** Distinguish the adversarial-ML attack classes and defenses.

```bash
python3 - <<'PY'
attacks = {"Evasion":"crafted input fools a model at inference -> robust training, input checks",
           "Poisoning":"corrupt training data -> data provenance + validation",
           "Model extraction":"query to steal a model -> rate limits + output limits",
           "Inversion/membership":"recover training data -> privacy (DP), minimize exposure"}
for a,d in attacks.items(): print(f"{a:22} -> {d}")
PY
```

**Expected result:** the adversarial-ML classes each with a defense — the OSAI ML
attack surface, oriented to controls.

**Negative test:** assume model accuracy equals security; a robust model still
needs **data provenance, rate limits, and privacy** controls.

**Cleanup:** none.

### Lab 8.3 — OSAI: the AI supply chain (concept)

**Objective:** Reason about model, dataset, and tool provenance.

```bash
python3 - <<'PY'
chain = {"Model":"verify source/signature; scan for unsafe serialization (e.g., pickle in weights)",
         "Dataset":"provenance + integrity; watch for poisoning",
         "Plugins/tools":"least privilege; the model's tools are its attack surface"}
for k,v in chain.items(): print(f"{k:12}: {v}")
PY
```

**Expected result:** the AI supply-chain components and their controls
(provenance, safe formats, least-privilege tools) — an OSAI area mirroring
software supply-chain security.

**Negative test:** load a model from an unverified source; unsafe weight formats
can execute code — verify provenance and use safe formats.

**Cleanup:** none.

### Lab 8.4 — OSAI: an AI red-team test plan (methodology)

**Objective:** Structure an authorized AI red-team engagement.

```bash
python3 - <<'PY'
plan = ["Scope + authorization (which model/app, which data, rules of engagement)",
        "Enumerate: inputs, tools/plugins, data sources, trust boundaries",
        "Test: prompt injection, jailbreaks, tool abuse, data leakage (authorized only)",
        "Report: findings + defenses (input trust, permissions, monitoring)"]
for s in plan: print("-", s)
PY
```

**Expected result:** an authorized AI red-team methodology (scope → enumerate →
test → report) — the OSAI engagement structure, authorization-first.

**Negative test:** probe a third-party AI service without authorization; AI red
teaming needs explicit permission like any test.

**Cleanup:** none.

### OSCE³ — Expert Track

### Lab 8.5 — OSCE³: map the expert path

**Objective:** Lay out the three credentials that earn OSCE³.

```bash
python3 - <<'PY'
osce3 = {"OSEP (PEN-300)":"advanced pentest / evasion",
         "OSWE (WEB-300)":"white-box web exploitation",
         "OSED (EXP-301)":"Windows exploit development"}
for cert,area in osce3.items(): print(f"{cert:16} -> {area}")
print("Hold all three -> OSCE3 (expert breadth). None of the three expire.")
PY
```

**Expected result:** the three 300-level credentials and the areas they cover,
combining into OSCE³ — the expert-track roadmap.

**Negative test:** expect a single OSCE³ exam; it is an **umbrella** earned by the
three separate credentials — plan them as a set.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

OSAI (AI-300) is OffSec's new AI Red Teamer credential — prompt injection,
adversarial ML, and the AI supply chain, each taught here with its defense — and
OSCE³ is the expert umbrella earned by holding OSEP, OSWE, and OSED. Both extend
the program to the frontier (AI) and the summit (expert breadth).

- [ ] I can name the three OSAI red-teaming areas and their defenses.
- [ ] I can explain prompt injection as an input-trust/permission problem.
- [ ] I can reason about AI supply-chain provenance.
- [ ] I can state how OSCE³ is earned and that its components don't expire.
- [ ] I completed Labs 8.1–8.5 including each negative test.
