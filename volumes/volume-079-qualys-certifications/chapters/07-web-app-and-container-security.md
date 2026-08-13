# Chapter 07: Web Application and Container Security

## Learning Objectives

- Scan web applications and APIs with TotalAppSec/WAS.
- Handle authenticated web scans safely.
- Secure containers and images with Container Security.
- Apply File Integrity Monitoring (FIM).
- Complete a walkthrough for each app/container topic.

## Theory and Architecture

Qualys extends assessment to applications and containers. **Web Application Scanning (WAS)** — part of
**TotalAppSec** — is a **DAST** engine that crawls and tests running web applications and **APIs** for
weaknesses (injection classes, authentication and session issues, misconfigurations, sensitive-data
exposure), with support for **authenticated** scans and careful scoping to avoid production impact.
**Container Security** secures the container lifecycle — scanning **images** in registries and CI/CD
for vulnerabilities before deployment, and monitoring **running containers** — because a vulnerable
base image propagates to every container built from it. **File Integrity Monitoring (FIM)** watches
critical files, directories, and registry keys for **unauthorized change** (a modified system binary,
an altered config), a key control for both security and compliance (PCI requires FIM). Together these
extend Qualys's coverage to **web apps, APIs, containers, and file integrity** — common breach vectors
that host scanning alone misses. This chapter teaches each with a hands-on defensive walkthrough (web
scoping, image scanning, and FIM).

## Design Considerations

**Scope** WAS to authorized apps, use **authenticated** scans, and include **APIs**. Scan container
**images in CI/CD** (shift left) and monitor runtime. Use **FIM** on critical files for change
detection and PCI. Prioritize **internet-facing** app findings. Integrate into the unified risk view.

## Implementation and Automation

The labs scope a web/API scan, scan a container image, and configure FIM.

## Validation and Troubleshooting

Confirm the app/container model:

```text
TotalAppSec/WAS = DAST for web apps + APIs (authenticated, scoped). Container Security = scan images in registries/CI-CD + monitor runtime (a vulnerable base image spreads). FIM = watch critical files/keys for unauthorized change (security + PCI).
Extends coverage to apps, APIs, containers, and file integrity.
```

Common pitfalls: an **unscoped** WAS scan hitting production; and scanning only running containers,
not the **images** they came from.

## Security and Best Practices

**Scope** web/API scans, **shift-left** image scanning in CI/CD, monitor runtime, and use **FIM** on
critical files. Prioritize internet-facing findings. All work is defensive and authorized.

## Hands-On Lab

App/container walkthroughs. **Shared prerequisites** — `python3`, in a lab (no live production).
**Cost:** none.

### Lab 7.1 — Scope a web/API scan

**Objective:** Scan safely and authorized.

```python
python3 - <<'PY'
scan={"target":"https://staging.myapp.example (authorized)","api":"OpenAPI/Swagger definition provided",
      "auth":"test account (authenticated)","exclusions":["/admin/purge"],"rate":"throttled"}
for k,v in scan.items(): print(f"{k:10}: {v}")
print("WAS/TotalAppSec: authorized target, API definition, authenticated + throttled, exclusions")
PY
```

**Expected result:** a **scoped, authenticated** web+API scan on an authorized target — safe WAS.

**Negative test:** scan production with no scope/exclusions; you risk impact — **scope** it.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 7.2 — Scan a container image (shift left)

**Objective:** Catch vulnerabilities before deploy.

```python
python3 - <<'PY'
image={"name":"myapp:1.4","base":"debian:11","vulns":[{"pkg":"openssl","sev":"Critical"}],"stage":"CI build"}
gate = not any(v["sev"]=="Critical" for v in image["vulns"])
print("image:", image["name"], "-> build gate:", "PASS" if gate else "FAIL (critical vuln in base image)")
print("Container Security: scan images in CI/CD; fail the build on critical vulns")
PY
```

**Expected result:** the build **failed** on a critical vulnerability in the base image — shift-left
container security.

**Negative test:** scan only running containers; the vulnerable **base image** already shipped — scan
images in **CI/CD**.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 7.3 — Configure File Integrity Monitoring

**Objective:** Detect unauthorized change.

```python
python3 - <<'PY'
baseline={"/etc/passwd":"hash-a","/bin/login":"hash-b"}
current ={"/etc/passwd":"hash-a","/bin/login":"hash-XX"}   # binary changed!
for path,h in baseline.items():
    if current[path]!=h: print(f"FIM ALERT: {path} changed ({h} -> {current[path]})")
print("FIM: unauthorized change to a system binary = high-priority alert (security + PCI)")
PY
```

**Expected result:** the **FIM alert** on the changed system binary — file-integrity monitoring.

**Negative test:** monitor only for known malware signatures; **FIM** catches unexpected changes to
trusted files — use it.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 7.4 — Prioritize internet-facing app findings

**Objective:** Fix the most exposed first.

```python
python3 - <<'PY'
findings=[{"app":"public-portal","exposure":"internet","sev":"High"},
          {"app":"internal-tool","exposure":"internal","sev":"High"}]
for f in sorted(findings,key=lambda x:x["exposure"]!="internet"):
    print(f"{f['app']:14} {f['exposure']:8} {f['sev']} -> {'fix first' if f['exposure']=='internet' else 'later'}")
PY
```

**Expected result:** the **internet-facing** app finding prioritized — exposure-weighted app
remediation.

**Negative test:** treat internet and internal findings equally; the **internet-facing** one is more
exposed — prioritize it.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

TotalAppSec/WAS tests authorized web apps and APIs (DAST), Container Security scans images in CI/CD and
runtime, and FIM detects unauthorized file change — extending Qualys coverage to apps, APIs,
containers, and integrity.

- [ ] I can scope a web/API scan.
- [ ] I can scan a container image (shift left).
- [ ] I can configure File Integrity Monitoring.
- [ ] I can prioritize internet-facing findings.
- [ ] I completed Labs 7.1–7.4 including each negative test.
