# Chapter 04: ACA — Cloud Security

## Learning Objectives

- Control access with Resource Access Management (RAM).
- Protect workloads with Security Center.
- Defend web apps with WAF.
- Mitigate volumetric attacks with Anti-DDoS.
- Complete a walkthrough for each cloud-security topic — defensively.

## Theory and Architecture

The **ACA Cloud Security** domain covers protecting an Alibaba Cloud tenancy — entirely **defensive**.
**RAM (Resource Access Management)** is Alibaba's identity and access service (the IAM equivalent):
**users**, **groups**, and **roles** are granted **policies** (JSON documents listing allowed actions
on resources) following least privilege, with **MFA** for sensitive access. **Security Center** (the
evolution of Server Guard) provides workload protection — vulnerability detection, baseline checks,
intrusion detection, and alerting across ECS instances. **WAF (Web Application Firewall)** protects
web applications from common attacks (injection, cross-site scripting) at the HTTP layer with managed
and custom rules. **Anti-DDoS** mitigates volumetric denial-of-service attacks — **Anti-DDoS Basic**
provides baseline protection, and **Anti-DDoS Pro/Premium** scrubs large attacks. Together, RAM
controls **who** can do what, Security Center protects the **workloads**, WAF protects the **apps**,
and Anti-DDoS protects **availability** — layered, defensive cloud security. This chapter teaches each
with a hands-on defensive walkthrough (RAM policy, Security Center, WAF, and DDoS reasoning).

> **Scope.** Cloud security here is **defensive** — controlling access, protecting workloads and apps,
> and mitigating attacks on your own tenancy. No lab is an attack.

## Design Considerations

Grant **least-privilege RAM** policies (specific actions/resources), require **MFA** for privileged
users, and avoid using the root account. Enable **Security Center** across workloads. Protect
internet-facing apps with **WAF**. Enable **Anti-DDoS** appropriate to exposure. Log and audit
(ActionTrail). Defense in depth.

## Implementation and Automation

The labs write a RAM policy, apply Security Center, and reason about WAF/DDoS.

## Validation and Troubleshooting

Confirm the cloud-security model:

```text
RAM = identity/access (users/groups/roles + JSON policies, least privilege, MFA). Security Center = workload protection (vuln/baseline/intrusion detection). WAF = web-app HTTP protection. Anti-DDoS Basic/Pro = volumetric attack mitigation.
Layered: RAM (who) + Security Center (workloads) + WAF (apps) + Anti-DDoS (availability).
```

Common pitfalls: using the **root account** for daily work (use least-privilege RAM); and internet-
facing apps with no **WAF/Anti-DDoS**.

## Security and Best Practices

Use least-privilege **RAM** with **MFA**, enable **Security Center**, protect apps with **WAF** and
availability with **Anti-DDoS**, and audit with ActionTrail. Defense in depth. All work is defensive.

## Hands-On Lab

Cloud-security walkthroughs. **Shared prerequisites** — `python3`; aliyun CLI optional. **Cost:** none.

### Lab 4.1 — Write a least-privilege RAM policy

**Objective:** Grant only what's needed.

```python
python3 - <<'PY'
import json
policy={"Version":"1","Statement":[{"Effect":"Allow","Action":["oss:GetObject","oss:PutObject"],
        "Resource":"acs:oss:*:*:acme-backups/*"}]}
print(json.dumps(policy,indent=2))
print("RAM: allow only OSS read/write on ONE bucket (least privilege) — not '*'")
PY
```

**Expected result:** a **RAM policy** scoped to one bucket and two actions — least privilege.

**Negative test:** grant `Action:"*"` on `Resource:"*"`; that's admin everywhere — scope to the
**specific** actions/resources.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 4.2 — Apply Security Center protection

**Objective:** Protect workloads.

```python
python3 - <<'PY'
posture={"agent":"installed on all ECS","vuln_scan":"weekly","baseline":"CIS check",
         "intrusion_detection":"enabled (alerts on webshell/brute-force)","response":"alert SOC + isolate"}
for k,v in posture.items(): print(f"{k:20}: {v}")
print("Security Center: continuous vuln + baseline + intrusion detection across workloads")
PY
```

**Expected result:** **Security Center** protecting workloads (vuln/baseline/intrusion) — cloud
workload security.

**Negative test:** rely on the perimeter alone; **Security Center** detects intrusions on the hosts —
enable it.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 4.3 — Protect a web app with WAF

**Objective:** Block web attacks.

```python
python3 - <<'PY'
def waf(request):
    if "' OR 1=1" in request or "<script>" in request: return "BLOCK (injection/XSS signature)"
    return "allow"
print("GET /search?q=laptop ->", waf("laptop"))
print("GET /search?q=' OR 1=1 ->", waf("' OR 1=1"))
print("WAF: managed rules block common web attacks at the HTTP layer")
PY
```

**Expected result:** the injection attempt **blocked** by WAF, legitimate traffic allowed — web-app
protection.

**Negative test:** put a public web app behind no **WAF**; common attacks reach it — enable WAF.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 4.4 — Plan Anti-DDoS protection

**Objective:** Protect availability.

```python
python3 - <<'PY'
tiers={"internal app (no public exposure)":"Anti-DDoS Basic (baseline)",
       "public web business":"Anti-DDoS Pro (scrubbing, higher capacity)",
       "high-value target (gaming/finance)":"Anti-DDoS Premium (global scrubbing)"}
for exposure,tier in tiers.items(): print(f"{exposure:36}: {tier}")
PY
```

**Expected result:** Anti-DDoS tier matched to **exposure** — availability protection.

**Negative test:** leave a high-value public service on **Basic** only; a large attack overwhelms it —
use **Pro/Premium**.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

ACA Cloud Security layers RAM least-privilege access, Security Center workload protection, WAF web-app
defense, and Anti-DDoS availability protection — defensive, defense-in-depth security for the tenancy.

- [ ] I can write a least-privilege RAM policy.
- [ ] I can apply Security Center protection.
- [ ] I can protect a web app with WAF.
- [ ] I can plan Anti-DDoS protection.
- [ ] I completed Labs 4.1–4.4 including each negative test.
