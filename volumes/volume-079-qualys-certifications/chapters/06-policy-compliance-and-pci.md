# Chapter 06: Policy Compliance and PCI

## Learning Objectives

- Assess configuration compliance with Policy Compliance.
- Map controls to benchmarks (CIS, DISA STIG) and mandates.
- Run PCI compliance and ASV scans.
- Report and remediate compliance gaps.
- Complete a walkthrough for each compliance topic.

## Theory and Architecture

Beyond vulnerabilities, Qualys assesses **configuration compliance** — whether systems are hardened
to a standard. **Policy Compliance (PC)** performs **credentialed** checks against **controls** (e.g.,
"password minimum length ≥ 14", "guest account disabled") organized into **policies** that map to
recognized benchmarks (**CIS Benchmarks**, **DISA STIGs**) and regulatory mandates (PCI DSS, HIPAA,
NIST, ISO). Each control is evaluated **pass/fail** per asset, producing a posture report and a
remediation list. **PCI Compliance** is a specialized module for the **Payment Card Industry Data
Security Standard**, including **ASV (Approved Scanning Vendor)** external scans required for
merchants, self-assessment questionnaires, and compliance reporting. Compliance answers a different
question than vulnerability management — "are we configured correctly and can we prove it to
auditors?" — and both are essential to a defensible security posture. This chapter teaches each with
a hands-on defensive walkthrough (control evaluation, benchmark mapping, and PCI reasoning).

## Design Considerations

Base policies on recognized **benchmarks** (CIS/STIG) and map to your **mandates**. Use
**credentialed** PC scans for accuracy. Prioritize **failed controls** on critical/regulated assets.
For PCI, schedule required **ASV** scans and track remediation to passing. **Report** posture for
auditors. Remediate and re-assess.

## Implementation and Automation

The labs evaluate a control, map to benchmarks, and reason about PCI/ASV.

## Validation and Troubleshooting

Confirm the compliance model:

```text
Policy Compliance = credentialed control checks (pass/fail) mapped to benchmarks (CIS/DISA STIG) + mandates (PCI/HIPAA/NIST/ISO). PCI module = PCI DSS + ASV external scans + SAQ + reporting.
Answers: "configured correctly + provable to auditors?" Complements vulnerability management.
```

Common pitfalls: **uncredentialed** compliance scans (can't read config accurately); and treating
compliance as a **one-time** audit instead of continuous.

## Security and Best Practices

Use **credentialed** PC scans against **benchmark-based** policies, prioritize **failed controls** on
regulated assets, run required **ASV** scans for PCI, and **report** for auditors. Remediate and
re-assess continuously. All work is defensive.

## Hands-On Lab

Compliance walkthroughs. **Shared prerequisites** — `python3`, in a lab. **Cost:** none.

### Lab 6.1 — Evaluate a compliance control

**Objective:** Pass/fail a hardening check.

```python
python3 - <<'PY'
controls=[{"id":"CIS 1.1.1","desc":"password min length >= 14","actual":12,"required":14},
          {"id":"CIS 2.3.1","desc":"guest account disabled","actual":"disabled","required":"disabled"}]
for c in controls:
    ok = (isinstance(c["actual"],int) and c["actual"]>=c["required"]) or c["actual"]==c["required"]
    print(f"{c['id']} [{'PASS' if ok else 'FAIL'}] {c['desc']} (actual={c['actual']})")
PY
```

**Expected result:** each control evaluated **pass/fail** — Policy Compliance assessment.

**Negative test:** self-attest to compliance without **evidence**; PC provides the **pass/fail
evidence** — assess it.

**Cleanup:** none.

### Lab 6.2 — Map controls to a benchmark

**Objective:** Base policy on a standard.

```python
python3 - <<'PY'
policy={"benchmark":"CIS Microsoft Windows Server 2022","mandate_mapping":["PCI DSS 2.2","NIST 800-53 CM-6"],
        "controls":42,"applies_to":"tag:Windows-Servers"}
for k,v in policy.items(): print(f"{k:16}: {v}")
print("Policy Compliance: policies from CIS/STIG benchmarks, mapped to mandates for audit")
PY
```

**Expected result:** a policy **based on a benchmark** and mapped to mandates — standards-based
compliance.

**Negative test:** write ad-hoc controls with no benchmark; auditors want **recognized standards** —
use CIS/STIG.

**Cleanup:** none.

### Lab 6.3 — Reason about PCI and ASV

**Objective:** Meet PCI requirements.

```python
python3 - <<'PY'
pci={"external_scan":"ASV (Approved Scanning Vendor) quarterly - required for merchants",
     "internal_scan":"internal vulnerability scans","saq":"self-assessment questionnaire",
     "goal":"pass ASV (no failing vulnerabilities) + document compliance"}
for k,v in pci.items(): print(f"{k:14}: {v}")
print("PCI module: ASV external scans must pass; track remediation to compliance")
PY
```

**Expected result:** the **PCI/ASV** requirements — the PCI compliance path.

**Negative test:** run any internal scan and call it PCI-compliant; PCI requires **ASV** external
scans — use the ASV process.

**Cleanup:** none.

### Lab 6.4 — Prioritize failed controls

**Objective:** Fix the riskiest gaps first.

```python
python3 - <<'PY'
failures=[{"control":"TLS 1.0 enabled","asset":"pci-web","regulated":True},
          {"control":"screensaver timeout","asset":"lab-pc","regulated":False}]
for f in sorted(failures,key=lambda x:not x["regulated"]):
    print(f"{f['control']:20} on {f['asset']:8} regulated={f['regulated']} -> {'fix first' if f['regulated'] else 'later'}")
PY
```

**Expected result:** the failed control on a **regulated** asset prioritized — risk-based compliance
remediation.

**Negative test:** fix compliance failures alphabetically; a **regulated** PCI failure waits —
prioritize by regulation/risk.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Policy Compliance evaluates configuration against CIS/STIG benchmarks and mandates with pass/fail
control checks, and the PCI module adds required ASV external scans — proving systems are hardened and
compliant, complementing vulnerability management.

- [ ] I can evaluate a compliance control.
- [ ] I can map controls to a benchmark.
- [ ] I can reason about PCI and ASV.
- [ ] I can prioritize failed controls.
- [ ] I completed Labs 6.1–6.4 including each negative test.
