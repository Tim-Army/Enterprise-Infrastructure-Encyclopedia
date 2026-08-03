# Chapter 07: Automation, Observability, and AIOps Certifications

## Learning Objectives

- Map the automation portfolio: Cloud Pak for Business Automation, Business Automation Workflow, FileNet, Datacap, and Turbonomic.
- Map the observability/AIOps portfolio: Instana and Cloud Pak for AIOps.
- Complete walkthrough labs on the concepts these certifications test.

## The portfolio

| Certification | Catalog code | Product |
|:---|:---|:---|
| Certified Cloud Pak for Business Automation v24.0.0 Solution Architect - Professional | Cert-C9007800 | CP4BA (automation platform) |
| Certified Business Automation Workflow v25.0.0 Developer - Professional | Cert-C9008800 | BAW (workflow/BPM) |
| Certified Deployment Professional - FileNet P8 V5.5.3 | Cert-C0004702 | FileNet (ECM) |
| Certified Turbonomic ARM v8.x Administrator - Professional | Cert-C9008100 | Turbonomic (resource mgmt) |
| Certified Instana Observability v1.0.277 Administrator - Professional | Cert-C9007500 | Instana (APM/observability) |
| Certified Cloud Pak for AIOps v4.6 Administrator - Professional | Cert-C9007400 | CP4AIOps (AIOps) |
| *Retiring soon:* Certified Developer - Datacap V9.1.8 | Cert-27004103 | Datacap (capture) |
| *Retiring soon:* Certified Administrator - Cloud Pak for Business Automation v21.0.3 | Cert-C9004400 | CP4BA (prior version) |

Two arcs: **automation** (workflow, content, capture, resource optimization) and **observability/AIOps** (seeing the estate and acting on it automatically).

## Hands-On Lab

Walkthroughs model the concepts with free primitives; products are design-level. **Cost:** none.

### Lab 7.1 — Workflow as a state machine (BAW Developer)

**Objective:** Build the process model BAW/BPM is built on.

```python
python3 - <<'EOF'
# A claim workflow: states, transitions, and a human task
transitions = {"Submitted":["Under Review"], "Under Review":["Approved","Rejected"],
               "Approved":["Paid"], "Rejected":[], "Paid":[]}
def advance(state, choice):
    return choice if choice in transitions[state] else state
s = "Submitted"
for choice in ["Under Review","Approved","Paid"]:
    s = advance(s, choice); print("->", s)
print("terminal?" , not transitions[s])
EOF
```

**Expected result:** The claim walks `Submitted → Under Review → Approved → Paid` and reports terminal — processes as states, transitions, tasks (human and system), and gateways is BPM's model; the BAW Developer exam tests building exactly this in the product.

**Negative test:** Attempt an illegal transition (`Submitted → Paid`) — it is refused; process definitions constrain paths, the property that makes workflow auditable.

**Cleanup:** None.

### Lab 7.2 — Content and capture (FileNet Deployment / Datacap Developer)

**Objective:** Separate the content repository from the capture pipeline.

```text
filenet p8> the ECM repository: documents + properties + folders, versioning, security, retention;
            content deployed and administered (the Deployment Professional credential)
datacap> the capture front end: scan -> OCR/recognize -> validate -> export INTO an ECM like FileNet
         (the Developer credential — retiring soon)
```

**Expected result:** The pipeline: **Datacap captures** (scan/OCR/validate), **FileNet stores and governs** (repository, retention, security). Datacap's credential is flagged retiring — note it but don't build a career plan on it.

**Negative test:** Expecting FileNet to OCR scanned paper — that is capture's job (Datacap); the repository governs what capture delivers.

**Cleanup:** None (design).

### Lab 7.3 — CP4BA platform composition (CP4BA Solution Architect)

**Objective:** State what the automation platform bundles.

```text
cp4ba (v24.0.0)> OpenShift-packaged: workflow (BAW) + content (FileNet) + decisions (ODM/business rules)
                 + capture + RPA + process mining — the architect composes these into a solution
```

**Expected result:** Cloud Pak for Business Automation as the umbrella that unifies workflow, content, decisions, capture, and RPA on OpenShift — the current Solution Architect credential (v24.0.0) is design; the older v21.0.3 Administrator credential is retiring.

**Negative test:** Treating CP4BA as one product — the architect exam tests choosing and composing its capabilities per requirement.

**Cleanup:** None (design).

### Lab 7.4 — Resource optimization (Turbonomic Administrator)

**Objective:** State Turbonomic's decision model.

```text
turbonomic (ARM v8.x)> continuously matches workload demand to resource supply, generating actions
   (resize, move, start/stop) to keep apps performant while cutting waste — "application resource management"
```

**Expected result:** Turbonomic as the closed loop from telemetry to *actions* (resize/move/place) that trade performance against cost — the Administrator exam tests configuring the analysis, action modes (recommend vs automate), and targets.

**Negative test:** Confusing Turbonomic (acts on resources) with pure monitoring (reports only) — the action generation is the product's point.

**Cleanup:** None (design).

### Lab 7.5 — Observability signals (Instana Administrator)

**Objective:** Exercise the three-signals model Instana is built on.

```bash
python3 - <<'EOF'
# Traces, metrics, logs — a request producing all three (the observability triad)
import time
t0=time.time()
# ... simulated work ...
latency_ms=(time.time()-t0)*1000+42
print(f"METRIC http.latency={latency_ms:.0f}ms")
print("TRACE spanId=abc parent=root service=checkout op=POST/pay duration_ms=%.0f" % latency_ms)
print("LOG level=INFO msg='payment ok' traceId=abc")
EOF
```

**Expected result:** One request emitting a **metric**, a **trace span**, and a **log** correlated by trace id — Instana's automatic-instrumentation model unifies exactly these; the Administrator exam tests agents, the service/endpoint map, and correlation.

**Negative test:** Metrics with no trace correlation — you see *that* latency rose but not *where*; correlation across signals is observability's value, and the exam tests it.

**Cleanup:** None.

### Lab 7.6 — AIOps correlation (Cloud Pak for AIOps Administrator)

**Objective:** State how AIOps reduces alert noise to incidents.

```python
python3 - <<'EOF'
# AIOps: correlate a storm of alerts into one probable incident
alerts = ["db latency high","checkout errors","cart timeouts","payment 500s"]
# temporal + topological correlation groups them; a single incident with a probable root:
print(f"INCIDENT: {len(alerts)} correlated alerts -> probable root: database latency")
EOF
```

**Expected result:** Four alerts collapsed into one incident with a probable root cause — Cloud Pak for AIOps applies ML to correlate events across topology and time, suppress noise, and suggest remediation; the Administrator exam tests connecting data sources, training/tuning the models, and runbook automation.

**Negative test:** Routing every raw alert to on-call — the noise AIOps exists to eliminate; correlation before notification is the design.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] Automation portfolio (CP4BA, BAW, FileNet, Datacap, Turbonomic) mapped, retiring items flagged.
- [ ] Workflow state-machine, content-vs-capture, and resource-action models drilled.
- [ ] Observability triad (Instana) and AIOps correlation (CP4AIOps) exercised.
