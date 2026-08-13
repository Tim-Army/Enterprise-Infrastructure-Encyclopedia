# Chapter 08: CCCS — Certified Cloud Specialist

## Learning Objectives

- Explain what the CCCS certifies and its target role.
- Summarize the seven exam-guide domains.
- Register cloud accounts and apply Falcon Cloud Security policies.
- Apply pre-runtime and runtime protection and remediate findings.
- Complete a per-domain walkthrough for each CCCS domain.

## Theory and Architecture

The **CrowdStrike Certified Cloud Specialist (CCCS)** validates managing **Falcon
Cloud Security** — the cloud-security-engineer credential. Its exam guide (90
minutes, 60 questions) covers **seven domains**: **Falcon Cloud Security Features and
Services**, **Cloud Account Registration**, **Cloud Security Policies and Rules**,
**Pre-Runtime Protection**, **Runtime Protection**, **Findings and Detection
Analysis**, and **Remediating and Reporting Issues**. Falcon Cloud Security spans
**CSPM**, **CWP**, and **CIEM** across AWS, Azure, and GCP.

## Design Considerations

The cloud specialist **registers** cloud accounts (read-only CSPM and/or sensor/
agent-based CWP), applies **policies/rules** for posture, enforces **pre-runtime**
controls (IaC scanning, image assessment, admission control) and **runtime**
protection (the sensor/Kubernetes protection agent), triages **findings/detections**,
and **remediates and reports**. Registration is the gate — no coverage without it.

## Implementation and Automation

The labs use Falcon Cloud Security and FalconPy for each domain — features,
registration, policies, pre-runtime, runtime, findings, and remediation.

## Validation and Troubleshooting

Confirm the exam guide before studying:

```text
crowdstrike.com > CCCS exam guide:
  1 Features and Services  2 Cloud Account Registration  3 Policies and Rules
  4 Pre-Runtime Protection  5 Runtime Protection
  6 Findings and Detection Analysis  7 Remediating and Reporting Issues
```

Common pitfalls: registering an account but not enabling **runtime** protection; and
IaC/image issues shipped because **pre-runtime** scanning was skipped.

## Security and Best Practices

Register **all** cloud accounts, combine **CSPM** (posture) with **CWP** (workloads)
and **CIEM** (entitlements), shift left with **pre-runtime** (IaC/image/admission),
protect running workloads with **runtime** agents, triage **findings** by risk, and
**remediate + report** with clear ownership.

## References and Knowledge Checks

- crowdstrike.com: CCCS exam guide; Falcon Cloud Security (CSPM/CWP/CIEM) docs.

**Knowledge checks**

1. What is the difference between pre-runtime and runtime protection?
2. Why is account registration the foundation?
3. What do CSPM, CWP, and CIEM each cover?

## Hands-On Lab

Per-domain walkthroughs — CCCS. **Shared prerequisites** — a Falcon tenant with Cloud
Security, a cloud account to register, `crowdstrike-falconpy`, and credentials.
**Cost:** none beyond the tenant/cloud free tier.

### Lab 8.1 — Features and Services

**Objective:** Enumerate registered cloud accounts and posture services.

```python
from falconpy import CSPMRegistration
c = CSPMRegistration(client_id=CID, client_secret=SEC)
acct = c.get_cloud_accounts()
print("registered cloud accounts:", len(acct["body"]["resources"]))
```

**Expected result:** the count of registered accounts across CSP(s) — the Features
and Services domain (what Cloud Security manages).

**Negative test:** assume full coverage; **enumerate accounts** — unregistered
accounts are invisible.

**Rollback:** none (read-only).

### Lab 8.2 — Cloud Account Registration

**Objective:** Register a cloud account for CSPM.

```python
r = c.create_aws_account(body={"resources":[{
  "account_id":"123456789012","cloudtrail_region":"us-east-1"}]})
print("registration status:", r["status_code"])
```

**Expected result:** a **201/200** registering the AWS account for posture management
— the Cloud Account Registration domain.

**Negative test:** monitor a cloud from outside; **register** it so Falcon has
API/role access to assess it.

**Rollback:** `c.delete_aws_account(ids=["123456789012"])` if it was for the lab.

### Lab 8.3 — Cloud Security Policies and Rules

**Objective:** List posture policy settings.

```python
pol = c.get_policy_settings()
print("posture policies:", len(pol["body"]["resources"]))
```

**Expected result:** the CSPM **policy/rule** set (misconfiguration checks) — the
Policies and Rules domain.

**Negative test:** accept defaults blindly; **tune policies** to your compliance
framework (CIS, PCI, etc.).

**Rollback:** none (read-only).

### Lab 8.4 — Pre-Runtime Protection

**Objective:** Assess a container image before deployment.

```bash
# Image Assessment at build time (CI): scan for vulns/misconfig before push
# falcon-imagescan --image myrepo/app:1.0 --report
echo "pre-runtime: IaC scanning + image assessment + admission control"
```

**Expected result:** an image/IaC assessment gating deployment — the Pre-Runtime
Protection domain (shift-left).

**Negative test:** scan only in production; **pre-runtime** catches issues before they
ship — scan in CI.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 8.5 — Runtime Protection

**Objective:** Confirm runtime protection on workloads/Kubernetes.

```python
from falconpy import Hosts
h = Hosts(client_id=CID, client_secret=SEC)
k8s = h.query_devices_by_filter(filter="service_provider:'AWS_EC2_V2'+platform_name:'Linux'")
print("cloud workloads with sensor:", len(k8s["body"]["resources"]))
```

**Expected result:** cloud workloads reporting the **sensor** (runtime CWP) — the
Runtime Protection domain.

**Negative test:** rely on CSPM posture alone; **runtime** protection detects active
threats in workloads — deploy the agent.

**Rollback:** none (read-only).

### Lab 8.6 — Findings and Detection Analysis

**Objective:** Review cloud misconfiguration/behavioral findings.

```python
find = c.get_configuration_detections()
print("cloud findings:", len(find["body"]["resources"]))
```

**Expected result:** the list of cloud **findings/detections** by severity — the
Findings and Detection Analysis domain.

**Negative test:** chase every finding equally; **prioritize by severity/exposure**
(public + privileged first).

**Rollback:** none (read-only).

### Lab 8.7 — Remediating and Reporting Issues

**Objective:** Produce a remediation guidance report for a finding.

```python
det = c.get_configuration_detections()["body"]["resources"]
if det:
    print("remediation:", det[0].get("remediation","see finding detail"))
```

**Expected result:** actionable **remediation guidance** for a finding — the
Remediating and Reporting Issues domain.

**Negative test:** close findings without a fix; **remediate + report** with owner and
evidence to actually reduce risk.

**Rollback:** none (read-only).

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The CCCS certifies Falcon Cloud Security across seven domains: features/services,
account registration, policies/rules, pre-runtime protection (IaC/image), runtime
protection (CWP), findings/detection analysis, and remediation/reporting — spanning
CSPM, CWP, and CIEM.

- [ ] I can enumerate and register cloud accounts.
- [ ] I can tune posture policies and rules.
- [ ] I can apply pre-runtime and runtime protection.
- [ ] I can triage findings and produce remediation reports.
- [ ] I completed Labs 8.1–8.7 including each negative test.
