# Chapter 06: Cloud Security

## Learning Objectives

- Apply cloud security essentials across providers (GCLD).
- Automate secure cloud with DevSecOps guardrails (GCSA).
- Respond to cloud incidents forensically (GCFR).
- Defend web applications (GWEB).
- Complete a walkthrough for each Cloud Security domain.

## Theory and Architecture

The **Cloud Security** focus area validates securing cloud workloads. **GCLD (Cloud Security
Essentials)** covers multi-cloud fundamentals — identity, network, storage, and the **shared
responsibility model** across AWS/Azure/GCP. **GCSA (Cloud Security Automation)** covers
**DevSecOps** — embedding security into CI/CD with policy-as-code, IaC scanning, and automated
guardrails so misconfigurations are caught before deployment. **GCFR (Cloud Forensics Responder)**
covers **incident response and forensics in the cloud** — collecting logs (CloudTrail/Activity
logs), reconstructing activity across ephemeral resources, and multi-cloud evidence. **GWEB (Web
Application Defender)** covers **defending** web apps — secure headers, input handling, and
mitigations for common weakness classes. A newer **GCTD (Cloud Threat Detection)** extends detection
into cloud telemetry, and **GCPN (Cloud Penetration Tester)** and **GCAD (Cloud Architecture &
Design)** round out the area. This chapter teaches each with a hands-on defensive walkthrough using
IaC/policy scanning, log analysis, and secure configuration.

## Design Considerations

Understand the **shared responsibility** boundary per service (GCLD). Shift security **left** with
IaC scanning and policy-as-code (GCSA). Ensure cloud **audit logs** are enabled and centralized for
forensics (GCFR). Defend web apps with **secure defaults** — headers, validation, least privilege
(GWEB). Detect on **cloud-native telemetry**, not just host logs.

## Implementation and Automation

The labs check shared responsibility, scan IaC, analyze a cloud log, and set secure headers.

## Validation and Troubleshooting

Confirm the Cloud Security map:

```text
GCLD = multi-cloud essentials + shared responsibility. GCSA = DevSecOps (IaC scan, policy-as-code, guardrails).
GCFR = cloud IR/forensics (CloudTrail/Activity logs, ephemeral resources). GWEB = web app defense (headers/validation).
```

Common pitfalls: assuming the provider secures **your** data/config (it doesn't — shared model); and
enabling audit logs **after** an incident (too late for forensics).

## Security and Best Practices

Know the **shared responsibility** line, scan IaC **before** deploy, enable and centralize **audit
logs** in advance, and defend web apps with secure defaults. Automate guardrails. All work is
defensive.

## Hands-On Lab

Cloud Security walkthroughs. **Shared prerequisites** — Linux with `python3`, `jq`; cloud CLIs
optional. **Cost:** none.

### Lab 6.1 — GCLD: apply the shared responsibility model

**Objective:** Assign each control to a party.

```python
python3 - <<'PY'
resp={"physical datacenter":"provider","hypervisor":"provider","guest OS patching (IaaS)":"customer",
      "IAM policy":"customer","data encryption/classification":"customer","managed DB engine (PaaS)":"provider"}
for item,who in resp.items(): print(f"{item:32}: {who}")
print("GCLD: the customer always owns identity, data, and configuration")
PY
```

**Expected result:** each control assigned to **provider or customer** — the shared-responsibility
model.

**Negative test:** assume the provider patches your **IaaS guest OS**; that's the **customer's** job
— know the boundary per service model.

**Cleanup:** none.

### Lab 6.2 — GCSA: scan infrastructure-as-code for misconfig

**Objective:** Catch a cloud misconfig before deploy.

```python
python3 - <<'PY'
# Toy IaC (Terraform-like) and a policy check (what checkov/tfsec do)
iac={"aws_s3_bucket":{"acl":"public-read","encryption":False}}
findings=[]
if iac["aws_s3_bucket"]["acl"].startswith("public"): findings.append("S3 bucket is PUBLIC")
if not iac["aws_s3_bucket"]["encryption"]: findings.append("S3 bucket unencrypted")
print("policy-as-code findings:", findings or "none")
print("GCSA: fail the pipeline on findings -> misconfig never reaches production")
PY
```

**Expected result:** the scan flags a **public, unencrypted bucket** — a DevSecOps guardrail (GCSA).

**Negative test:** deploy IaC with no scan; the public bucket ships and leaks — **scan in the
pipeline** first.

**Cleanup:** none.

### Lab 6.3 — GCFR: analyze a cloud audit log

**Objective:** Reconstruct cloud activity.

```bash
cat > /tmp/trail.json <<'JSON'
[{"eventName":"ConsoleLogin","sourceIP":"203.0.113.9","mfa":false,"user":"root"},
 {"eventName":"CreateAccessKey","sourceIP":"203.0.113.9","user":"root"}]
JSON
jq -r '.[] | "\(.eventName)\tuser=\(.user)\tip=\(.sourceIP)\tmfa=\(.mfa // "-")"' /tmp/trail.json
echo "GCFR: root login w/o MFA + new access key from same IP = suspicious sequence"
```

**Expected result:** the parsed **CloudTrail-style** events showing a root login without MFA then a
new key — cloud forensics (GCFR).

**Negative test:** investigate a cloud incident with audit logging **disabled**; there's no trail —
enable it **before** you need it.

**Cleanup:** `rm -f /tmp/trail.json`.

### Lab 6.4 — GWEB: set secure response headers

**Objective:** Defend a web app by default.

```python
python3 - <<'PY'
headers={"Content-Security-Policy":"default-src 'self'","X-Content-Type-Options":"nosniff",
         "Strict-Transport-Security":"max-age=31536000","X-Frame-Options":"DENY"}
for h,v in headers.items(): print(f"{h}: {v}")
print("GWEB: secure headers mitigate whole classes of web attacks by default")
PY
```

**Expected result:** a set of **secure HTTP headers** (CSP, HSTS, nosniff, frame-deny) — GWEB
defense-by-default.

**Negative test:** ship with no CSP/HSTS and "fix later"; whole weakness classes stay open — set
**secure defaults** from the start.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Cloud Security spans multi-cloud essentials and shared responsibility (GCLD), DevSecOps automation
(GCSA), cloud forensics/response (GCFR), and web-app defense (GWEB) — knowing the boundary, scanning
IaC early, logging in advance, and defending by default.

- [ ] I can apply the shared responsibility model (GCLD).
- [ ] I can scan IaC for misconfig (GCSA).
- [ ] I can analyze a cloud audit log (GCFR).
- [ ] I can set secure web headers (GWEB).
- [ ] I completed Labs 6.1–6.4 including each negative test.
