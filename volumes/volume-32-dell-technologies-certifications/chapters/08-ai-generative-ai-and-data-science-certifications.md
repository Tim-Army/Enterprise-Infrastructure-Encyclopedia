# Chapter 08: AI, Generative AI, and Data Science Certifications

## Learning Objectives

- Position Dell's AI certification set: GenAI Foundations
  (D-GAI-F-01), Prompt Engineering (D-PEN-F-A-00), Agentic AI
  Foundations (D-AAI-FN-A-00), AI Security (D-AIS-F-A-00), and the
  data-science trio (D-DS-FN-23, D-DS-OP-23, D-AA-OP-23)
- Connect the credentials to the infrastructure they assume: XE
  servers (Chapter 02), PowerScale data lakes (Chapter 04), and the
  NVIDIA-partnered validated designs
- Understand the AI-infrastructure content Dell co-badges with
  NVIDIA and where those externally-delivered credentials fit
- Build the study path from GenAI literacy to agentic patterns with
  this encyclopedia's Volumes VIII/IX/XI as the systems substrate

## Theory and Architecture

### What Dell certifies here

This family certifies **literacy and applied judgment**, not model
mathematics: GenAI Foundations covers the transformer-era vocabulary,
use-case framing, and the lifecycle from data to deployment; Prompt
Engineering certifies the craft of instructing models (patterns,
evaluation, failure modes); Agentic AI Foundations covers the 2026
frontier — tool-using, multi-step agent systems and their control
loops; AI Security addresses the new attack surface (prompt
injection, data leakage, model supply chain). The data-science trio
predates the GenAI wave: DS Foundations, Data Engineering Optimize,
and Data Science Optimize certify the pipeline-and-model craft on
which the newer credentials stand.

### The infrastructure story underneath

Dell's AI curriculum assumes its hardware story: XE-class GPU servers
(Chapter 02), PowerScale/ECS feeding data pipelines (Chapter 04),
and validated designs with NVIDIA — whose own associate credentials
(AI Infrastructure and Operations; GenAI and LLMs) Dell's program
points to for the accelerator-stack depth. Study them as one stack:
Dell certifies the platform and applied layers, NVIDIA the
accelerator specifics.

### Agentic AI, honestly framed

The agentic credential's substance is systems engineering: bounded
tools, verification gates, audit trails, and failure containment —
the same doctrines Volumes IX (automation trust ladders) and XI
(observability) teach for any autonomous system. Candidates strong in
those volumes find the exam's judgment questions familiar.

## Design Considerations

- Sequence: GenAI Foundations → Prompt Engineering → Agentic AI,
  with AI Security alongside for anyone touching production; the
  data-science trio only where the role builds pipelines/models
- Infrastructure candidates pair this chapter with XE Install/Operate
  rather than the DS trio
- Treat vendor AI claims with the currency discipline this repo
  practices: this family changes faster than any other Dell track —
  re-verify codes at registration

## Implementation and Automation

```text
# The study lab is this encyclopedia's own stack:
# - Volume VIII: serve a small open model behind an API on the K8s lab
# - Volume IX: wrap it in a pipeline with eval gates (the PE exam's
#   evaluation mindset, executed)
# - Volume XI: trace/token telemetry as observability practice
# - Agentic drill: a two-tool agent (search + calculator) with
#   logged decisions, a max-step budget, and a human gate — the
#   AAI blueprint's control loop in 200 lines
```

## Validation and Troubleshooting

- Evaluate prompts like software: fixed test suites, regression on
  every change — "it seemed better" is the failure mode the PE exam
  exists to end
- Agent failures triage in order: tool contract, context assembly,
  stop conditions — before model quality
- AI Security drills: attempt prompt injection against your own lab
  agent and document the mitigation that held

## Security and Best Practices

- Secrets never in prompts; retrieval scopes enforced server-side;
  model and dataset provenance recorded (supply chain)
- Log every agent action with inputs/outputs for audit; rate and
  budget limits as hard controls
- The D-AIS-F-A-00 blueprint doubles as a checklist for any GenAI
  deployment this encyclopedia's readers ship

## References and Knowledge Checks

- Exam descriptions: D-GAI-F-01, D-PEN-F-A-00, D-AAI-FN-A-00,
  D-AIS-F-A-00, D-DS-FN-23, D-DS-OP-23, D-AA-OP-23 (Dell Learning
  catalog); NVIDIA's partnered associate certifications
- Volumes VIII, IX, XI of this encyclopedia as the systems substrate

Knowledge checks:

1. Separate what Dell certifies from what NVIDIA certifies in the
   joint AI story.
2. Name three agentic-system controls that predate GenAI and where
   this encyclopedia teaches them.
3. Why do prompt-engineering exams emphasize evaluation over
   phrasing?

## Hands-On Lab

Run the four-part study lab from Implementation on the existing lab
stack: served model, evaluated prompt suite (10 cases, scored before
and after one change), the two-tool agent with logged runs and a
demonstrated stop condition, and one successful-then-mitigated
prompt-injection attempt — a portfolio artifact per credential.

## Lab Verification

Verification means all four artifacts exist with evidence (eval
scores, agent logs showing the gate and budget firing, the injection
transcript with its fix), reproducible from the repo's lab volumes.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

- [ ] All seven AI/DS codes recorded from the verified table
- [ ] Dell/NVIDIA certification seam articulated
- [ ] Prompt-eval and agent-control artifacts produced
- [ ] AI Security mitigations demonstrated on own lab
