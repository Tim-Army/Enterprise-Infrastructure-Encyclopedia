# Chapter 07: CIS — Security Operations and GRC

## Learning Objectives

- Orchestrate Vulnerability Response (VR).
- Manage Security Incident Response (SIR).
- Implement Integrated Risk Management (IRM / Risk & Compliance).
- Automate security workflows defensively.
- Complete a walkthrough for each SecOps/GRC domain.

## Theory and Architecture

ServiceNow's **Security Operations (SecOps)** and **Governance, Risk, and Compliance (GRC)**
applications bring security and risk workflows onto the platform — **defensively**, orchestrating
detection, prioritization, and response, never attacking. **Vulnerability Response (CIS-VR)** ingests
findings from scanners (Tenable, Qualys, Rapid7), correlates them to **CMDB CIs** and business
context, prioritizes by risk, and drives **remediation** through change/task workflows — closing the
loop between scanning and IT. **Security Incident Response (CIS-SIR)** manages the security-incident
lifecycle (detection → analysis → containment → eradication → recovery), integrating with SIEM/EDR and
automating enrichment and response (playbooks). **Integrated Risk Management (IRM, formerly GRC —
CIS-RC)** manages **policies, controls, risks, and compliance** — mapping controls to authorities
(NIST, ISO, PCI), running assessments, and tracking findings. The common thread is **workflow
orchestration**: turning security and risk data into tracked, automated, auditable action on an
authorized platform. This chapter teaches each with a hands-on defensive walkthrough (vulnerability
prioritization, incident lifecycle, and control mapping).

> **Scope.** SecOps and GRC here are **defensive** — orchestrating authorized detection,
> prioritization, response, and compliance workflows on your own instance. No lab is an attack.

## Design Considerations

Ingest scanner findings and correlate to **CMDB/business context** for risk-based **VR**
prioritization. Run **SIR** through the full incident lifecycle with **playbook** automation. Map
**IRM** controls to authorities and automate assessments. Integrate with existing security tools.
Keep everything **auditable**. Defensive orchestration only.

## Implementation and Automation

The labs prioritize a vulnerability, run an incident playbook, and map a control.

## Validation and Troubleshooting

Confirm the SecOps/GRC model:

```text
VR (CIS-VR): ingest scanner findings -> correlate to CMDB/business context -> prioritize -> drive remediation (change/task). SIR (CIS-SIR): security-incident lifecycle + SIEM/EDR integration + playbooks.
IRM/RC (CIS-RC): policies/controls/risks/compliance mapped to authorities (NIST/ISO/PCI) + assessments + findings. All defensive orchestration.
```

Common pitfalls: treating **VR findings** as a flat list (no CMDB/business context = poor
prioritization); and **SIR** with no playbook (slow, inconsistent response).

## Security and Best Practices

Prioritize **VR** by CMDB/business context, run **SIR** with playbooks, map **IRM** controls to
authorities, integrate security tools, and keep audit trails. Everything is **defensive** workflow
orchestration on an authorized instance.

## Hands-On Lab

SecOps/GRC walkthroughs. **Shared prerequisites** — `python3`, a free PDI. **Cost:** none.

### Lab 7.1 — Prioritize a vulnerability (VR)

**Objective:** Risk-based remediation.

```python
python3 - <<'PY'
findings=[{"cve":"CVE-A","cvss":9.8,"ci":"internal-lab","business":"low"},
          {"cve":"CVE-B","cvss":7.2,"ci":"payment-prod","business":"critical","exploited":True}]
def score(f): return f["cvss"]*(3 if f.get("business")=="critical" else 1)*(2 if f.get("exploited") else 1)
for f in sorted(findings,key=lambda x:-score(x)):
    print(f"{f['cve']} on {f['ci']:14} biz={f['business']:8} -> score {score(f):.0f}")
print("VR: correlate CVSS + CMDB/business context + exploitation -> risk-based order")
PY
```

**Expected result:** the exploited vuln on the **critical payment CI** prioritized over a higher-CVSS
lab finding — VR risk-based prioritization.

**Negative test:** remediate by **CVSS alone**; you fix the lab box before payment-prod — add
**business/CMDB context**.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 7.2 — Run a Security Incident playbook (SIR)

**Objective:** Consistent incident response.

```python
python3 - <<'PY'
phases=["Detection (SIEM alert)","Analysis (enrich: user/asset/IOC)","Containment (isolate host)",
        "Eradication (remove artifacts)","Recovery (restore)","Post-incident (lessons)"]
for i,p in enumerate(phases,1): print(f"{i}. {p}")
print("SIR: a playbook automates enrichment + drives the incident lifecycle consistently")
PY
```

**Expected result:** the SIR **incident lifecycle** as an automated playbook — consistent response.

**Negative test:** handle each security incident ad hoc; response is slow and inconsistent — use a
**playbook**.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 7.3 — Map an IRM control

**Objective:** Tie controls to compliance.

```python
python3 - <<'PY'
control={"id":"AC-2 (Account Management)","authority":["NIST 800-53","ISO 27001 A.9"],
         "test":"quarterly access review evidence","status":"needs assessment"}
for k,v in control.items(): print(f"{k:9}: {v}")
print("IRM/RC: map controls to authorities (NIST/ISO/PCI) + assess + track findings for audit")
PY
```

**Expected result:** a **control** mapped to authorities with an assessment — IRM compliance.

**Negative test:** track compliance in spreadsheets with no **authority mapping**; audits need
traceability — map controls in IRM.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 7.4 — Close the VR-to-change loop

**Objective:** Drive remediation to done.

```python
python3 - <<'PY'
vuln={"cve":"CVE-B","ci":"payment-prod","fix":"apply patch KB123"}
flow=["VR item prioritized","create change request (linked CI)","CAB approval","patch deployed","re-scan confirms fixed","VR item closed"]
for i,s in enumerate(flow,1): print(f"{i}. {s}")
print("VR: orchestrate remediation as a tracked change -> verified closure (loop closed)")
PY
```

**Expected result:** the vulnerability driven through a **tracked change** to verified closure —
VR/ITSM integration.

**Negative test:** email IT to "please patch" with no tracking; it stalls — orchestrate a **change**
and verify.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

CIS SecOps (VR, SIR) and IRM/GRC bring defensive security and risk workflows onto the platform —
risk-based vulnerability prioritization, playbook-driven incident response, and control-to-authority
compliance mapping — orchestrating authorized, auditable action.

- [ ] I can prioritize a vulnerability (VR).
- [ ] I can run a Security Incident playbook (SIR).
- [ ] I can map an IRM control.
- [ ] I can close the VR-to-change loop.
- [ ] I completed Labs 7.1–7.4 including each negative test.
