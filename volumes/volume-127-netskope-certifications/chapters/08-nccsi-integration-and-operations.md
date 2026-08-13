# Chapter 08: NCCSI — Integration and Operations

## Learning Objectives

- Cover the NCCSI's integration pillar: SSO/SAML, REST API, IaaS/SSPM, and advanced analytics.
- Understand how Netskope fits into an enterprise's identity, automation, and cloud-posture stack.
- Model SAML-based identity steering and API-driven automation.

## The exam in brief

**NCCSI** (Netskope Certified Cloud Security Integrator) certifies deeper, **integration-level** skill — the **Netskope One Professional** course is the prep. Where NCCSA administers the platform, NCCSI **connects it to the enterprise**: identity (SAML/SSO), automation (REST API), cloud posture (IaaS security, SSPM), advanced DLP, and analytics. Its topics (per the training outline): Risk Insights, IaaS, SAML, Advanced DLP, Netskope for Web, and the REST API.

## Hands-On Lab

Python and free primitives model identity and API integration. **Cost:** none.

### Lab 8.1 — SAML identity for steering and policy

**Objective:** Model how user identity enters Netskope for identity-aware policy.

```bash
python3 - <<'EOF'
# SAML SSO: the IdP asserts user identity + attributes; Netskope uses them in policy
saml_assertion = {"user":"alice@corp.com", "groups":["finance","employees"], "device":"managed"}
def policy(assertion, app):
    if "finance" in assertion["groups"] and app == "erp": return "ALLOW (finance group)"
    if app == "erp": return "DENY (not in finance group)"
    return "ALLOW"
print("alice -> erp:", policy(saml_assertion, "erp"))
print("bob(no finance) -> erp:", policy({"user":"bob@corp.com","groups":["employees"],"device":"managed"}, "erp"))
EOF
```

**Expected result:**

```text
alice -> erp: ALLOW (finance group)
bob(no finance) -> erp: DENY (not in finance group)
```

SAML SSO brings **identity and group attributes** from the IdP (Okta, Entra ID, Ping) into Netskope, so policy is user/group-aware, not IP-based. Integrating the IdP — SAML forward proxy, SCIM provisioning — is a core NCCSI skill.

**Negative test:** Policy by IP/subnet instead of SAML identity — you can't distinguish alice from bob on the same network; identity integration is what makes user-aware policy possible.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 8.2 — REST API automation

**Objective:** Model automating Netskope with its REST API.

```bash
python3 - <<'EOF'
# Netskope REST API pattern: pull events, push policy/config as code
import json
# GET /api/v2/events/dataexport (modeled): retrieve DLP incidents for a SIEM
events = [{"type":"dlp","user":"alice","file":"customers.xlsx","severity":"high","action":"blocked"}]
print("SIEM export:", json.dumps(events[0]))
# POST config (modeled): add a URL to a custom block list programmatically
new_block = {"list":"corp-blocklist","add":["malware-x.example"]}
print("automated policy update:", json.dumps(new_block))
print("NCCSI: integrate via API -> SIEM/SOAR, IaC policy, automated incident export")
EOF
```

**Expected result:** Event export and programmatic policy update via the API — NCCSI expects you to integrate Netskope into the security operations stack: export events/incidents to a SIEM, drive policy as code, and automate response with SOAR. The REST API is the integration surface.

**Negative test:** Managing everything by hand in the console at enterprise scale — no repeatability, no SIEM correlation; the API is what makes Netskope an integrated part of the SOC, which the exam tests.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 8.3 — IaaS security and SSPM (cloud posture)

**Objective:** Understand Netskope's posture-management surface beyond inline traffic.

```bash
python3 - <<'EOF'
# CSPM/SSPM: continuously check cloud & SaaS CONFIGURATION for misconfigurations
checks = [
  ("S3 bucket public read", "FAIL", "high"),
  ("IAM user without MFA", "FAIL", "high"),
  ("SaaS admin without MFA (SSPM)", "FAIL", "high"),
  ("Encryption at rest enabled", "PASS", "-"),
]
for check, result, sev in checks:
    flag = "  <-- remediate" if result == "FAIL" else ""
    print(f"[{result}] {check} (sev {sev}){flag}")
EOF
```

**Expected result:** Configuration checks flagging public buckets, missing MFA, and SaaS misconfigurations — **CSPM** (cloud infrastructure posture) and **SSPM** (SaaS security posture) find risky *configuration*, complementing the inline data/threat controls. NCCSI covers these posture surfaces as part of a complete cloud-security integration.

**Negative test:** Inline DLP/threat protection alone misses a publicly-exposed storage bucket (a configuration problem, not a traffic problem); posture management (CSPM/SSPM) is the control for that class of risk.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 8.4 — Advanced analytics and Risk Insights

**Objective:** Model turning telemetry into risk intelligence.

```bash
python3 - <<'EOF'
# Advanced Analytics / Risk Insights: aggregate events into risk signals (e.g. UEBA)
user_events = {"alice":{"downloads_gb":2,"failed_logins":1,"new_country":False},
               "mallory":{"downloads_gb":80,"failed_logins":9,"new_country":True}}
def risk(e):
    score = e["downloads_gb"] + e["failed_logins"]*5 + (30 if e["new_country"] else 0)
    return score, ("HIGH — investigate" if score > 50 else "normal")
for u,e in user_events.items():
    s, verdict = risk(e); print(f"{u:<8} risk={s:<4} {verdict}")
EOF
```

**Expected result:**

```text
alice    risk=7    normal
mallory  risk=125  HIGH — investigate
```

Advanced Analytics and **Risk Insights** turn raw events into risk scores and UEBA-style signals — mass downloads plus failed logins plus a new country flags a likely compromised account or insider. NCCSI covers reading and integrating this intelligence (dashboards, SIEM export) for detection and compliance.

**Negative test:** Looking at raw events without aggregation — the mass-download-plus-anomaly pattern is invisible one event at a time; analytics is what surfaces the risk, and the exam expects you to use it.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] SAML/SSO identity integration for user-aware policy modeled.
- [ ] REST API automation (SIEM export, policy-as-code) drilled.
- [ ] IaaS/SSPM posture management and Advanced Analytics/Risk Insights understood.
