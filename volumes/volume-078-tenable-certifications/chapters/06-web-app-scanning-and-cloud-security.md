# Chapter 06: Web Application Scanning and Cloud Security

## Learning Objectives

- Scan web applications with Tenable Web App Scanning (WAS).
- Handle authenticated web scans and scope safely.
- Assess cloud posture with Tenable Cloud Security.
- Detect cloud misconfigurations and toxic combinations.
- Complete a walkthrough for each WAS/Cloud topic.

## Theory and Architecture

Two products extend Tenable beyond host and network scanning. **Web Application Scanning (WAS)** is a
**DAST (Dynamic Application Security Testing)** engine that crawls and tests running web applications
for weaknesses (injection classes, authentication issues, misconfigurations, exposed data) — from the
outside, like an attacker, but **authorized**. WAS handles **authenticated** scans (logging in to
test protected functionality) and must be **scoped** carefully to avoid destructive actions on
production. **Tenable Cloud Security** (a **CSPM/CNAPP** capability) assesses cloud environments
(AWS/Azure/GCP) for **misconfigurations** — public storage, over-permissive IAM, unencrypted data,
open security groups — and identifies **toxic combinations** (e.g., a public workload with an admin
role and a known vulnerability) that together create real attack paths. Both extend the exposure
picture: **web apps** and **cloud posture** are common breach vectors that host scanning alone misses.
This chapter teaches each with a hands-on defensive walkthrough (safe web scoping, and cloud misconfig
and attack-path analysis).

## Design Considerations

**Scope** WAS carefully — authorized apps, test environments where possible, avoid destructive
payloads. Use **authenticated** WAS to reach protected functionality. For cloud, assess against
**benchmarks** (CIS) and hunt **toxic combinations**, not just single misconfigs. Prioritize
**internet-exposed** issues. Integrate findings into the unified exposure view.

## Implementation and Automation

The labs scope a web scan, interpret WAS findings, check cloud posture, and find a toxic combination.

## Validation and Troubleshooting

Confirm the WAS/Cloud model:

```text
WAS = DAST for running web apps (crawl + test; authenticated scans; scope carefully). Cloud Security = CSPM/CNAPP: misconfig detection (public storage/over-permissive IAM/open SG) + toxic combinations (attack paths).
Both extend exposure beyond hosts to web apps and cloud posture.
```

Common pitfalls: an **unscoped** WAS scan hitting production destructively; and treating single cloud
misconfigs in isolation while missing **toxic combinations**.

## Security and Best Practices

**Scope** web scans to authorized apps, use **authenticated** scans, assess cloud against **CIS
benchmarks**, and prioritize **toxic combinations** and internet-exposed issues. All work is defensive
and authorized.

## Hands-On Lab

WAS/Cloud walkthroughs. **Shared prerequisites** — `python3`, in a lab (no live production targets).
**Cost:** none.

### Lab 6.1 — Scope a web application scan

**Objective:** Scan safely and authorized.

```python
python3 - <<'PY'
scan={"target":"https://staging.myapp.example (authorized)","excluded":["/admin/delete","/payment"],
      "auth":"test account (authenticated crawl)","rate":"throttled to avoid impact"}
for k,v in scan.items(): print(f"{k:10}: {v}")
print("WAS: authorized target, exclusions for destructive paths, authenticated + throttled")
PY
```

**Expected result:** a **scoped, authenticated, throttled** web scan on an authorized target — safe
WAS.

**Negative test:** point WAS at production with no exclusions or throttling; it may trigger destructive
actions or an outage — **scope** it.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 6.2 — Interpret a WAS finding

**Objective:** Turn a web finding into a fix.

```python
python3 - <<'PY'
finding={"type":"Reflected input not sanitized","location":"/search?q=","severity":"High",
         "fix":"server-side input validation + output encoding + CSP"}
for k,v in finding.items(): print(f"{k:9}: {v}")
print("WAS: report weakness class + remediation for developers")
PY
```

**Expected result:** a WAS finding with a **remediation** for developers — actionable web results.

**Negative test:** hand developers raw scanner output with no fix guidance; it's not actionable —
include the **remediation**.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 6.3 — Check cloud posture (CSPM)

**Objective:** Detect cloud misconfigurations.

```python
python3 - <<'PY'
resources=[{"type":"s3","public":True,"encrypted":False},{"type":"iam_role","admin":True,"used_days":400},
           {"type":"security_group","open_ports":["0.0.0.0/0:22"]}]
findings=[]
for r in resources:
    if r.get("public"): findings.append(f"{r['type']} public")
    if r.get("encrypted") is False: findings.append(f"{r['type']} unencrypted")
    if r.get("admin") and r.get("used_days",0)>90: findings.append(f"{r['type']} unused admin role")
    if r.get("open_ports"): findings.append(f"{r['type']} SSH open to world")
print("cloud misconfigurations:", findings)
PY
```

**Expected result:** the cloud **misconfigurations** flagged (public/unencrypted/unused-admin/open-SSH)
— CSPM.

**Negative test:** assume the cloud provider secures your config; the **customer** owns it — assess
posture.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 6.4 — Find a toxic combination

**Objective:** Identify an attack path.

```python
python3 - <<'PY'
workload={"internet_facing":True,"has_critical_vuln":True,"attached_role":"admin","has_secrets":True}
toxic = workload["internet_facing"] and workload["has_critical_vuln"] and workload["attached_role"]=="admin"
print("workload:", workload)
print("verdict:", "TOXIC COMBINATION -> internet + critical vuln + admin role = real attack path (fix first)" if toxic else "lower risk")
PY
```

**Expected result:** the **toxic combination** (internet + vuln + admin role) surfaced as a top
priority — attack-path analysis.

**Negative test:** rank each misconfig alone by severity; the dangerous **combination** is missed —
analyze attack paths.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Web App Scanning (DAST) safely tests authorized running applications, and Cloud Security (CSPM/CNAPP)
detects cloud misconfigurations and toxic combinations — extending exposure management to web apps
and cloud posture.

- [ ] I can scope a web scan safely.
- [ ] I can interpret a WAS finding.
- [ ] I can check cloud posture.
- [ ] I can find a toxic combination.
- [ ] I completed Labs 6.1–6.4 including each negative test.
