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

This chapter carries a topic-level walkthrough lab for **each key product of the Security
Operations track (NSE 5–7)** — FortiAnalyzer, FortiSIEM, FortiSOAR, FortiEDR,
FortiSandbox, and FortiNDR — mapped in the volume README's coverage tables. The products
are SOC platforms driven by GUI, CLI, and API; each lab gives concrete, verifiable steps
and ends **`**Lab verified by:** *pending*`** until a human runs it.

**Shared prerequisites for Labs 12.1–12.5** — a FortiGate sending logs, plus the relevant
SOC product (FortiAnalyzer, FortiSIEM, FortiSOAR, FortiEDR/FortiSandbox, FortiNDR) as VM
or hardware, reachable on the management network. **Cost:** none beyond lab resources.

### Lab 12.1 — FortiAnalyzer log analytics (Topic: FortiAnalyzer)

**Objective:** Register the FortiGate and confirm logs are indexed for analytics.

```text
# On FortiGate: point logging at FortiAnalyzer
config log fortianalyzer setting
    set status enable
    set server 10.0.0.242
    set upload-option realtime
end
diagnose test application miglogd 6
# On FortiAnalyzer:
diagnose test application oftpd 3     # ADOM/device registration status
```

**Expected result:** the FortiGate appears as a registered device on FortiAnalyzer and
logs flow in real time; FortiView, reports, and FortiAI analytics populate — FortiAnalyzer
is the SOC's log store, correlation, and reporting hub.

**Negative test:** enable FortiAnalyzer logging but leave the device unauthorized on the
analyzer; logs are refused and analytics stay empty — device registration must be accepted.

**Rollback:** disable the FortiAnalyzer log setting if lab-only.

### Lab 12.2 — FortiSIEM correlation (Topic: FortiSIEM)

**Objective:** Confirm event ingestion and a correlation rule firing.

```text
# On FortiSIEM: add the FortiGate as a monitored device (discovery via SNMP/syslog), then:
#   Analytics > run a search:  eventType = "FortiGate-Traffic" AND action = "deny"
#   Confirm a built-in rule (e.g. "Excessive Denied Connections") triggers an incident.
phStatus                 # FortiSIEM CLI: verify all backend processes are up
```

**Expected result:** FortiSIEM ingests and parses FortiGate events, and a correlation
rule raises an incident when the pattern (many denies from one source) is met — SIEM turns
raw multi-source events into prioritized incidents with context.

**Negative test:** rely on a single log source for correlation; cross-source rules (auth +
traffic + endpoint) cannot fire — SIEM's value is correlating across the whole estate.

**Rollback:** none (read-only analytics).

### Lab 12.3 — FortiSOAR playbook (Topic: FortiSOAR)

**Objective:** Run a playbook that enriches and responds to an alert.

```text
# On FortiSOAR: open a sample "Phishing Email" alert, then run a playbook that:
#   1. extracts IOCs (URL, sender, attachment hash)
#   2. enriches via FortiGuard / threat-intel connector
#   3. on a malicious verdict, blocks the URL on FortiGate and closes the alert
# Verify in the playbook execution log that each step returned success.
```

**Expected result:** the playbook auto-enriches the alert, reaches a verdict, and pushes a
block to the FortiGate — SOAR codifies analyst runbooks so response is consistent and fast,
with the human approving high-impact steps.

**Negative test:** automate a destructive containment step with no approval gate; a
false-positive playbook run disrupts production — high-impact actions need a human-approval
task in the playbook.

**Rollback:** revert any test block pushed to the FortiGate.

### Lab 12.4 — Endpoint detection with FortiEDR and FortiSandbox (Topic: FortiEDR / FortiSandbox)

**Objective:** Detonate a suspicious file and read the verdict chain.

```text
# On FortiGate: forward suspicious files to FortiSandbox
config antivirus profile
    edit av-lab
        config http
            set av-scan enable
        end
        set analytics-db enable
    next
end
config system fortisandbox
    set status enable
    set server 10.0.0.243
end
diagnose test application quarantined-files 2>/dev/null | head
```

**Expected result:** unknown files are submitted to FortiSandbox for detonation; a
malicious verdict feeds back to block future instances, while FortiEDR catches the
behavior on the endpoint itself — layered detection across network and host.

**Negative test:** rely only on signature AV for a zero-day; it has no signature and passes
— sandbox detonation and EDR behavior analysis are what catch the unknown.

**Rollback:** disable the FortiSandbox integration if lab-only.

### Lab 12.5 — Network detection with FortiNDR (Topic: FortiNDR)

**Objective:** Confirm FortiNDR is analyzing mirrored traffic for anomalies.

```text
# Mirror traffic to FortiNDR (SPAN or FortiGate mirror), then on FortiNDR:
#   Dashboard > confirm flows are being classified by the neural-network engine
#   Review a detected anomaly (e.g. beaconing / lateral movement) with its evidence
diagnose netdetector status 2>/dev/null | head
```

**Expected result:** FortiNDR classifies mirrored traffic and surfaces behavior-based
detections (C2 beaconing, lateral movement, data exfiltration) that signature tools miss —
NDR adds the network-behavior layer to the SOC's detection coverage.

**Negative test:** feed FortiNDR no mirrored traffic and expect detections; with nothing to
analyze the dashboard is empty — NDR requires a traffic feed (SPAN/mirror) to work.

**Rollback:** remove the mirror configuration if lab-only.

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
