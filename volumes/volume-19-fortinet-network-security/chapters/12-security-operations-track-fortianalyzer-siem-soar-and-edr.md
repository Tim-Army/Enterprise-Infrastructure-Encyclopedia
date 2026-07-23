# Chapter 12: Security Operations Track — FortiAnalyzer, SIEM, SOAR, and EDR

## Learning Objectives

- Operate the Security Operations product estate: FortiAnalyzer
  (analytics), FortiSIEM (correlation), FortiSOAR (orchestration),
  FortiEDR (endpoint), FortiNDR (network detection), FortiSandbox,
  FortiDeceptor, FortiRecon
- Map the NSE 5–7 Security Operations ladder: FortiAnalyzer Analyst
  and FortiSandbox (NSE 5); FortiSIEM/FortiSOAR/FortiEDR/FortiNDR/
  FortiRecon (NSE 6); Security Operations Analyst and Architect (NSE 7)
- Build a Fortinet SOC that consolidates detection, investigation, and
  automated response
- Connect the track to this encyclopedia's SOC doctrine (Volumes X, XI)

## Theory and Architecture

### The track in one sentence

Security Operations certifies the Fortinet SOC: **FortiAnalyzer** as
the analytics-and-logging core, **FortiSIEM** for cross-source
correlation and CMDB-aware detection, **FortiSOAR** for
playbook-driven orchestration, and the detection sensors —
**FortiEDR** (endpoint), **FortiNDR** (network/AI), **FortiSandbox**
(detonation), **FortiDeceptor** (deception), **FortiRecon** (external
attack surface). The ladder runs FortiAnalyzer Analyst / FortiSandbox
at **NSE 5**, the sensor-and-orchestration estate at **NSE 6**, and
**Security Operations Analyst** and **Security Operations Architect**
at **NSE 7** (verified 22 July 2026).

### Analyst versus Architect, Fortinet edition

The Analyst role operates the SOC: triage in FortiAnalyzer/FortiSIEM,
investigate with the detection sensors' telemetry, and drive response
through FortiSOAR playbooks. The Architect designs it: data onboarding
strategy, correlation and detection engineering, playbook design, and
multi-product integration across the Security Fabric. The same
analyst/engineer/architect grammar as this encyclopedia's other SOC
volumes (XVI, X), in Fortinet products.

### The Security Fabric advantage

Fortinet's pitch is integration: FortiGate, FortiEDR, and FortiNDR feed
FortiAnalyzer/FortiSIEM, which trigger FortiSOAR playbooks that act
back through the fabric (block at the FortiGate, isolate via FortiEDR).
The NSE 7 exams reward understanding this closed loop — detection to
automated, fabric-wide response — not any single product in isolation.

## Design Considerations

- Onboard by detection value: FortiGate and endpoint (FortiEDR) logs
  before low-signal sources; parsing/normalization gates detection
- Automate enrichment and containment of unambiguous incidents; gate
  destructive actions behind analyst tasks (Volume IX's trust ladder,
  in FortiSOAR)
- FortiSIEM vs. FortiAnalyzer: Analyzer for Fortinet-centric analytics
  and reporting; SIEM where multi-vendor correlation and CMDB context
  are required — many SOCs run both
- Detection content is code: correlation rules and playbooks versioned
  and regression-tested

## Implementation and Automation

```text
# FortiAnalyzer / FortiSIEM investigation and FortiSOAR response
# 1. FortiAnalyzer: FortiView + log queries scope the incident
diagnose test application fortilogd 1      # log ingestion health
# 2. FortiSIEM: correlation rule fires -> incident with CMDB context
# 3. FortiSOAR playbook: enrich (threat intel) -> decide -> act
#    - auto: block IP at FortiGate via the fabric connector
#    - gated: FortiEDR host isolation waits for an analyst task
# FortiSOAR is API-first; playbooks call connectors, this repo's
# Volume IX pipeline governs their content lifecycle
```

## Validation and Troubleshooting

- Ingestion first: no logs, no detection — verify FortiAnalyzer/SIEM
  ingestion and parsing before tuning any rule
- Analyst triage order: incident → contributing events → affected
  assets (CMDB) → response, reading the platform timeline as truth
- FortiSOAR playbook failures triage in the task graph — connector
  auth, inputs, conditions — before blaming content
- FortiEDR/FortiNDR detections: validate sensor coverage completeness;
  gaps read as safety

## Security and Best Practices

- RBAC per role: analysts cannot alter detection content or fabric
  connectors; destructive response gated
- Fabric connector credentials are keys to enforcement points — vault
  and scope them
- Measure the SOC: auto-resolved incidents, analyst-hours saved, and
  automated actions later reversed (the false-positive tax)

## References and Knowledge Checks

- Fortinet Training Institute exam pages: FortiAnalyzer, FortiSandbox,
  FortiSIEM, FortiSOAR, FortiEDR, FortiNDR, FortiRecon, Security
  Operations Analyst/Architect (NSE 5–7 Security Operations)
- Product admin guides; Volumes X and XI of this encyclopedia

Knowledge checks:

1. Trace one incident from FortiGate log to automated, gated response
   across the Fortinet SOC, naming each product's role.
2. When do you run FortiSIEM alongside FortiAnalyzer, and why?
3. Which SOC actions belong on FortiSOAR's auto rung and which behind
   an analyst task?

## Hands-On Lab

In a Fortinet SOC lab (FortiAnalyzer VM + FortiGate VM, plus the free
NSE self-paced labs where available; else runbook): forward FortiGate
logs to FortiAnalyzer, build one FortiView-based investigation of a
seeded incident, and design a FortiSOAR playbook that auto-blocks a
malicious IP at the FortiGate and gates host isolation behind an
analyst task. Test against a true positive and a false-positive
control.

## Lab Verification

Verification means logs ingested and the incident scoped from real
data, the playbook auto-contained the true positive and held at the
analyst gate on the control, and every step is evidenced.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

- [ ] FortiAnalyzer/FortiSIEM investigation performed
- [ ] FortiSOAR playbook with auto and gated rungs built
- [ ] Detection-sensor roles (EDR/NDR/Sandbox) mapped to NSE levels
- [ ] SecOps NSE 5–7 ladder recorded from verified sources
