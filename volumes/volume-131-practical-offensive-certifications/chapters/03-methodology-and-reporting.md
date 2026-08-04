# Chapter 03: The Penetration Test Methodology and Reporting

## Learning Objectives

- Cover the engagement methodology these certifications assess (CPTS, PNPT, eCPPT) — scoping through reporting.
- Understand why the **report** is what these practical exams truly test.
- Build a report structure and a rules-of-engagement checklist.

## The exam is the engagement

The flagship practical certs — HTB **CPTS**, TCM **PNPT**, INE **eCPPT** — assess a full, authorized engagement: you get a scoped environment, work it over days, and **deliver a professional report**. The report is not an afterthought; it is often what separates a pass from a fail, because in real consulting **the report is the deliverable the client pays for.** A brilliant finding that isn't clearly communicated, risk-rated, and remediable is worthless.

## The methodology (authorized engagement)

| Phase | What happens | Governance |
|:---|:---|:---|
| **Pre-engagement / scoping** | Define targets, exclusions, timing, rules of engagement (RoE) | **Signed authorization** — the legal basis |
| **Reconnaissance** | Map the footprint ([Chapter 02](02-reconnaissance-and-osint.md)) | In-scope only |
| **Enumeration / analysis** | Identify services, versions, weaknesses | Non-destructive |
| **Exploitation** | Prove impact by demonstrating a vulnerability (in the authorized lab) | Within scope; avoid harm |
| **Post-exploitation** | Assess reachable impact (lateral movement, data at risk) | Scoped; documented |
| **Reporting** | Findings, risk ratings, evidence, **remediation** | The deliverable |
| **Remediation retest** | Verify fixes | Closes the loop |

## Hands-On Lab

Python models the RoE and report structure. **Cost:** none.

### Lab 3.1 — Rules of engagement checklist

**Objective:** Build the authorization/scope gate every engagement must pass first.

```bash
python3 - <<'EOF'
# No testing begins until every RoE item is confirmed — the legal/ethical gate
roe = {
  "signed authorization / SOW": False,
  "in-scope targets defined": True,
  "explicit exclusions listed": True,
  "test window (dates/hours)": True,
  "emergency contact + stop condition": False,
  "data-handling / evidence rules": True,
}
missing = [k for k, ok in roe.items() if not ok]
print("RoE readiness:")
for k, ok in roe.items(): print(f"  [{'x' if ok else ' '}] {k}")
print(f"\n{'DO NOT PROCEED — missing: ' + ', '.join(missing) if missing else 'READY — authorization and scope confirmed'}")
EOF
```

**Expected result:** The engagement is **blocked** — the signed authorization and stop condition are missing. The rules-of-engagement checklist is the gate: **no test begins without confirmed authorization, defined scope, and a stop condition.** These practical certs (and real engagements) treat this as foundational; an unauthorized or out-of-scope action is the cardinal failure.

**Negative test:** Starting testing with a verbal "sure, go ahead" and no signed scope — legally and professionally unacceptable; the signed authorization is what makes the work lawful, and its absence stops everything.

**Cleanup:** None.

### Lab 3.2 — Structure a professional report

**Objective:** Build the report skeleton these exams grade.

```bash
python3 - <<'EOF'
report = {
  "1. Executive Summary": "business-level: overall risk, key themes, for leadership (no jargon)",
  "2. Scope & Methodology": "what was tested, when, how, and the RoE",
  "3. Findings": "each: title, severity (CVSS + business context), affected assets, evidence, reproduction",
  "4. Remediation": "specific, actionable fixes prioritized by risk",
  "5. Appendices": "raw evidence, tool output, references",
}
for section, contents in report.items():
    print(f"{section}\n    {contents}")
print("\nThe report is the deliverable — a finding without clear evidence, risk rating, and a fix is incomplete.")
EOF
```

**Expected result:** A five-part report — executive summary (for leadership), scope/methodology, findings (with severity, evidence, reproduction), **remediation**, and appendices. Practical exams grade the report because it is the real product: a defender or client must be able to **understand, prioritize, and fix** each finding. The executive summary (business language) and per-finding remediation are what make it usable.

**Negative test:** A report that lists vulnerabilities with no severity, no evidence, and no remediation — it fails the exam and fails the client; communication and actionability are the point, not a raw scanner dump.

**Cleanup:** None.

### Lab 3.3 — Risk-rate a finding

**Objective:** Rate a finding by technical severity *and* business context.

```bash
python3 - <<'EOF'
# Severity blends CVSS-style technical score with business context (exploitability, exposure, asset value)
def rate(cvss, internet_facing, sensitive_data, exploit_available):
    score = cvss
    if internet_facing: score += 1.0
    if sensitive_data:  score += 1.0
    if exploit_available: score += 0.5
    score = min(score, 10.0)
    band = "LOW" if score < 4 else "MEDIUM" if score < 7 else "HIGH" if score < 9 else "CRITICAL"
    return round(score,1), band
print("SQLi on internet login, PII, public exploit:", rate(7.5, True, True, True))
print("Missing header on internal test box:        ", rate(3.1, False, False, False))
EOF
```

**Expected result:** The internet-facing SQL injection over PII with a public exploit rates CRITICAL; a missing header on an internal test box rates LOW. Good reporting **contextualizes** the technical score with exposure, data sensitivity, and exploit availability — so the client fixes the CRITICAL first. This risk-based prioritization is a core reporting skill these certs assess.

**Negative test:** Reporting every finding at the same severity (or by raw CVSS alone) — the client can't prioritize; business context is what turns a vulnerability list into an actionable risk report.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] The authorized-engagement methodology (scope → recon → analysis → demonstrate → report → retest) internalized.
- [ ] The RoE gate (no test without signed authorization + scope + stop condition) drilled.
- [ ] The professional report structure and business-context risk rating built.
